# ChatGPT Telegram bot

![python-version](https://img.shields.io/badge/python-3.8-blue.svg)
![playwright-version](https://img.shields.io/badge/revChatGPT-0.0.31.5-green.svg)](https://github.com/acheong08/ChatGPT)
![license](https://img.shields.io/badge/License-GPL%202.0-brightgreen.svg)](LICENSE)

## Requirements
- Python 3.8+ and Pipenv
- A telegram bot and it's token
- An openai account(or it's session key)

## Getting Start
### Install
1. clone this repo and move to the project folder
```
git clone https://github.com/miyago9267/auto-ai-chat-bot.git
cd auto-ai-chat-bot
```

2. Create a new virtual enviroment with Pipenv
```
pipenv install
pipenv shell
```

### Configure
Modified your own config by copying `.env.example` and rename it as  `.env`, then check your all config correct.
```
OPENAI_AUTH_KEY="<YOUR OPENAI AUTH KEY>"
TELEGRAM_BOT_TOKEN="<YOUR TELEGRAM BOT TOKEN>"
OPENAI_IMG_API_KEY="<YOUR OPENAI IMAGE GENERATE KEY>"
```

You need to provide:
1. Your openai chat auth key, u can get the key by following step
    1. login to the [ChatGPT OpenAi](https://chat.openai.com/chat), u can not only login using email but also goole or microsoft account
    2. Press your `F12`->`Application`->`Cookie`, and copy your `__Secure-next-auth.session-token` into the `.env` file
2. Your telegram token
3. An open ai image api key

### Run
run the `app.py`
```
python app.py
```