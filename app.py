from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaAudio, InputMediaDocument, InputMediaPhoto, InputMediaVideo
import telegram.constants
from dotenv import load_dotenv
from revChatGPT.revChatGPT import Chatbot
import requests as req
import json
import os

img_req_data = {
    'url': 'https://api.openai.com/v1/images/generations',
    'header': {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer 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'
    },
    'data': {
        "prompt": "",
        "n": 1, 
        "size": "1024x1024"
    }
}

media_type = {
    'A': InputMediaAudio,    # 聲音
    'D': InputMediaDocument, # 壓縮文件
    'P': InputMediaPhoto,    # 圖片
    'V': InputMediaVideo     # 影片
}

config = {
    'session_token': '',
}


def start(bot, update):
    global has_start
    if has_start:
        update.message.reply_text(text=
            '不需要Start第二次了啦>.<'
        )
        return
    update.message.reply_text(text=
        '歡迎使用AutoAIChatBot owo\n' + \
        '本機器人目前支援的指令有:\n\n' + \
        '/chat <text>: 透過Chat GPT api回應你的聊天\n' + \
        '/refresh: 重新整理ChatGPT AI的進程\n' + \
        '/get_img <tag>: 透過OpenAI圖片產生器api回應你一張圖片\n' + \
        '/help: 查看本幫助列表\n\n' + \
        '本bot由Miyago9267沒有贊助播出'
    )
    has_start = True

def help(bot, update):
    update.message.reply_text(text=
        '歡迎使用AutoAIChatBot owo\n' + \
        '本機器人目前支援的指令有:\n\n' + \
        '/chat <text>: 透過Chat GPT api回應你的聊天\n' + \
        '/refresh: 重新整理ChatGPT AI的進程\n' + \
        '/get_img <tag>: 透過OpenAI圖片產生器api回應你一張圖片\n' + \
        '/help: 查看本幫助列表\n\n' + \
        '本bot由Miyago9267沒有贊助播出'
    )

def chat(bot, update):
    global chatbot
    if update.message.text == '/chat':
        update.message.reply_text(text=
            '請跟AI說一些話喔owo'
        )
        return
    response = get_chatgpt_response(update.message.text[6:].replace('\n', ' '))
    bot.send_message(
            chat_id=update.effective_chat.id,
            reply_to_message_id=update.message.message_id,
            text=response['message']
    )
    # update.message.reply_text('sorry qwq, it\'s WOP')

def get_chatgpt_response(message) -> dict:
    global chatbot
    try:
        # print('Start get chat response')
        response = chatbot.get_chat_response(message)
        # print(response['message'])
        return response
    except Exception as e:
        print(e)
        return {"message": "I'm having some trouble talking to you, please try again later."}

def refresh(bot, update):
    global chatbot
    chatbot.refresh_session()
    bot.send_message(chat_id=update.effective_chat.id, text="Done!")

def get_img(bot, update):
    if update.message.text == '/get_img':
        update.message.reply_text(text=
            '請給我一個標籤才能產生圖片喔owo'
        )
        return
    img_req = update.message.text[9:].replace('\n', ' ')
    img_url = generate_img(img_req)
    # print(img_url)
    bot.send_photo(chat_id=update.message['chat']['id'], photo=img_url,
        reply_markup = InlineKeyboardMarkup([[
            InlineKeyboardButton(f'下載圖片', url = f'{img_url}'),
            InlineKeyboardButton('重新生成', callback_data=f'{img_req}')
        ]])
    )

def regenerate(bot, update):
    img_req = update.callback_query.data
    img_url = generate_img(img_req)
    bot.send_photo(chat_id=update.callback_query.message['chat']['id'], photo=img_url,
        reply_markup = InlineKeyboardMarkup([[
            InlineKeyboardButton(f'下載圖片', url = f'{img_url}'),
            InlineKeyboardButton('重新生成', callback_data=f'{img_req}')
        ]])
    )

def generate_img(prompt):
    global img_req_data
    result = ''
    img_req_data['data']['prompt'] = prompt
    res = [url['url'] for url in json.loads(req.post(img_req_data['url'], headers=img_req_data['header'], json=img_req_data['data']).text)['data']]
    for url in res:
        result += url
    return result

def main():
    global has_start, chatbot, config
    load_dotenv()
    config['session_token'] = os.getenv('OPENAI_AUTH_KEY')

    updater = Updater(os.getenv('TELEGRAM_BOT_TOKEN'), use_context=False)
    print('Bot is running...')

    chatbot = Chatbot(config, conversation_id=None)

    has_start = False

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(CommandHandler('chat', chat))
    updater.dispatcher.add_handler(CommandHandler('refresh', refresh))
    updater.dispatcher.add_handler(CommandHandler('get_img', get_img))
    updater.dispatcher.add_handler(CallbackQueryHandler(regenerate))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()