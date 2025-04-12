# Chittak (Claude 3 + NTFY)

A Python script that watches your screenshots folder, extracts the top-left task from new images using **Claude 3 Vision**, and sends the answer to your **ntfy.sh** channel.

---

## ⚙️ How It Works

1. Monitors `~/Pictures/Screenshots` for new screenshots.
2. Whenever a new screenshot is taken, it sends the image to Claude 3 with a prompt to identify the task in the image and return the solution.
3. Sends the answer to `ntfy.sh` topic, which will show up on phone.

---

## 🧩 Requirements

- Python 3.8+
- [Anthropic API key](https://www.anthropic.com/)
- A topic name for [ntfy.sh](https://ntfy.sh/)

## Setup

1. Run the following commands:
```bash
git clone git@github.com:bsuvonov/chittak.git
cd chittak
python3 -m venv env & source env/bin/activate
pip install -r requirements.txt
touch .env
```
2. Go to www.anthropic.com and get your API key.
3. Visit ntfy.sh, create an account, and set up a new topic.
4. Install the ntfy.sh app from app store on your phone and login to your account.
5. Add your credentials to the .env file like this:
  ```
  ANTHROPIC_API_KEY=<your-anthropic-api-key>
  NTFY_TOPIC=<your-ntfy-topic-name>
  ```
5. Go to www.anthropic.com and get an API key. Go to ntfy.sh, create an account and create a new topic. Put your anthropic API key and ntfy.sh topic name into .env file in this format:
```
ANTHROPIC_API_KEY=<your-anthropic-api-key>
NTFY_TOPIC=<your-ntfy-topic-name>
```

## How to use
1. Run the script on terminal:
```python
python main.py
```
2. Start your online exam.
3. Take a screenshot of the problem (make sure the entire problem fits on the screen).
4. Wait a few seconds — you’ll receive the solution directly on your phone via the ntfy.sh app.
