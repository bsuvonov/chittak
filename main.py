import requests
import anthropic
import base64
import time
import os
import subprocess
from dotenv import load_dotenv
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Load environment variables from .env
load_dotenv()
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
NTFY_TOPIC = os.getenv("NTFY_TOPIC")


class ImageHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            print(f"New image detected: {event.src_path}")
            self.process(event.src_path)

    def process(self, file_path):
        print("Processing the image...")

        with open(file_path, 'rb') as img_file:
            img = img_file.read()
        image1_media_type = "image/png"
        image1_data = base64.standard_b64encode(img).decode("utf-8")

        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        answer = client.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": image1_media_type,
                                "data": image1_data,
                            },
                        },
                        {
                            "type": "text",
                            "text": """In the image, there is a task for you. You should identify the task, and provide an answer. If you find multiple tasks, choose only one task that is located the toppest and most left in the image, and provide an answer to it.

                            Return only the task and answer with no other redundant text. Follow the examples on what to return:

                            Example 1 (multiple choice question):
                            Q: What is the capital of Uruguay?
                            A: a) Montevideo

                            Example 2 (general question):
                            Q: What is the law of relativity by Einstein?
                            A: The principle of relativity states that The laws of physics are the same for all observers in any inertial frame of reference relative to one another

                            Example 3 (coding problem):
                            Q: How do you print 'Hello World!' in C++?
                            A: #include <iostream>

                            int main(){
                                std::cout << "Hello World!" << std::endl;
                                return 0;
                            }
                            """
                        }
                    ],
                }
            ],
        )

        print("Answer:", answer.content[-1].text)
        requests.post(f'https://ntfy.sh/{NTFY_TOPIC}', answer.content[-1].text)


if __name__ == "__main__":
    path_to_watch = os.path.expanduser("~/Pictures/Screenshots")
    event_handler = ImageHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path_to_watch, recursive=False)
    observer.start()
    print(f"Monitoring folder: {path_to_watch}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping observer...")
        observer.stop()
    observer.join()
