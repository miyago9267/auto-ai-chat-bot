from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaAudio, InputMediaDocument, InputMediaPhoto, InputMediaVideo
import telegram.constants as constants
from asyncChatGPT.asyncChatGPT import Chatbot as ChatGPT3Bot
import asyncio
import requests as req
import json
import os

class TelegramBot:
    def __init__(self, config, chatbot):#: ChatGPT3Bot):
        self.updater = Updater(token=config['telegram_token'], use_context=False)
        self.chatbot = chatbot
        self.config = config
        
        self.has_start = False

        self.help_mes = '歡迎使用AutoAIChatBot owo\n' + \
            '本機器人目前支援的指令有:\n\n' + \
            '/chat <text>: 透過Chat GPT api回應你的聊天\n' + \
            '/refresh: 重新整理ChatGPT AI的進程\n' + \
            '/img <tag>: 透過OpenAI圖片產生器api回應你一張圖片\n' + \
            '/help: 查看本幫助列表\n\n' + \
            '本bot由Miyago9267沒有贊助播出'

        self.img_req_data = {
            'url': 'https://api.openai.com/v1/images/generations',
            'header': {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.config["api_key"]}'
            },
            'data': {
                "prompt": "",
                "n": 1, 
                "size": "1024x1024"
            }
        }

    def start(self, bot, update):
        if self.has_start:
            update.message.reply_text(text=
                '不需要Start第二次了啦>.<'
            )
            return
        update.message.reply_text(text=self.help_mes)
        self.has_start = True

    def help(self, bot, update):
        update.message.reply_text(text=self.help_mes)
        return

    def chat(self, bot, update):
        if update.message.text == '/chat':
            bot.send_message(text='請跟AI說一些話喔owo')
            return
        response = self.get_chatgpt_response(
            update.message.text[6:].replace('\n', ' ')
        )

        bot.send_message(
            chat_id=update.effective_chat.id,
            reply_to_message_id=update.message.message_id,
            text=response['message'],
            parse_mode=constants.PARSEMODE_MARKDOWN
        )
        # update.message.reply_text('sorry qwq, it\'s WIP')

    def get_chatgpt_response(self, message) -> dict:
        try:
            response = self.chatbot.get_chat_response(message)
            # print(message)
            return response
        except Exception as e:
            print(e)
            return {"message": "I'm having some trouble talking to you, please try again later."}

    def refresh(self, bot, update):
        self.chatbot.refresh_session()
        bot.send_message(chat_id=update.effective_chat.id, text="Done!")

    def get_img(self, bot, update, req=None):
        mes = update.message if req==None else update.callback_query.message
        if req==None and update.message.text == '/img':
            bot.send_message(text=
                '請給我一個標籤才能產生圖片喔owo'
            )
            return
        img_req = update.message.text[5:].replace('\n', ' ') if req==None else req
        img_url = self.generate_img(img_req)
        # print(img_url)
        bot.send_photo(
            chat_id=mes['chat']['id'],
            photo=img_url,
            reply_markup = InlineKeyboardMarkup([[
                InlineKeyboardButton(f'下載圖片', url = f'{img_url}'),
                InlineKeyboardButton('重新生成', callback_data=f'{img_req}')
            ]])
        )

    def regenerate(self, bot, update):
        img_req = update.callback_query.data
        self.get_img(bot, update, req=img_req)

    def generate_img(self, prompt):
        result = ''
        self.img_req_data['data']['prompt'] = prompt
        res = [url['url'] for url in json.loads(req.post(self.img_req_data['url'], headers=self.img_req_data['header'], json=self.img_req_data['data']).text)['data']]
        for url in res:
            result += url
        return result

    def run(self):
        print('Bot is running...')

        updater = self.updater

        updater.dispatcher.add_handler(CommandHandler('start', self.start))
        updater.dispatcher.add_handler(CommandHandler('help', self.help))
        updater.dispatcher.add_handler(CommandHandler('chat', self.chat))
        updater.dispatcher.add_handler(CommandHandler('refresh', self.refresh))
        updater.dispatcher.add_handler(CommandHandler('img', self.get_img))
        updater.dispatcher.add_handler(CallbackQueryHandler(self.regenerate))

        updater.start_polling()
        updater.idle()