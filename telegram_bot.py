from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaAudio, InputMediaDocument, InputMediaPhoto, InputMediaVideo
import telegram.constants
import requests as req
import json
import os

class TelegramBot:
    def __init__(self, config, chatbot):
        self.updater = Updater(token=token['telegram_token'], use_context=True)
        self.chatbot = chatbot
        self.config = config
        
        self.has_start = False

        self.help = '歡迎使用AutoAIChatBot owo\n' + \
            '本機器人目前支援的指令有:\n\n' + \
            '/chat <text>: 透過Chat GPT api回應你的聊天\n' + \
            '/refresh: 重新整理ChatGPT AI的進程\n' + \
            '/get_img <tag>: 透過OpenAI圖片產生器api回應你一張圖片\n' + \
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

    async def start(self, bot, update):
        if self.has_start:
            await update.message.reply_text(text=
                '不需要Start第二次了啦>.<'
            )
            return
        await help(bot, update)
        self.has_start = True

    async def help(self, bot, update):
        await update.message.reply_text(text=self.help)

    async def chat(self, update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.text == '/chat':
            update.message.reply_text(text=
                '請跟AI說一些話喔owo'
            )
            return
        response = await get_chatgpt_response(update.message.text[6:].replace('\n', ' '))
        typing_task.cancel()

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            reply_to_message_id=update.message.message_id,
            text=response['message'],
            parse_mode=constants.ParseMode.MARKDOWN
        )
        # update.message.reply_text('sorry qwq, it\'s WOP')

    async def get_chatgpt_response(message):
        try:
            response = await self.chatbot.get_chat_response(message)
            return response
        except Exception as e:
            print(e)
            return {"message": "I'm having some trouble talking to you, please try again later."}

    async def refresh(self, bot, update):
        self.chatbot.refresh_session()
        await bot.send_message(chat_id=update.effective_chat.id, text="Done!")

    async def get_img(self, bot, update, req=None):
        if update.message.text == '/get_img':
            await update.message.reply_text(text=
                '請給我一個標籤才能產生圖片喔owo'
            )
            return
        img_req = update.message.text[9:].replace('\n', ' ') if req==None else req
        img_url = await generate_img(img_req)
        # print(img_url)
        await bot.send_photo(
            hat_id=update.message['chat']['id'],
            photo=img_url,
            reply_markup = InlineKeyboardMarkup([[
                InlineKeyboardButton(f'下載圖片', url = f'{img_url}'),
                InlineKeyboardButton('重新生成', callback_data=f'{img_req}')
            ]])
        )

    async def regenerate(self, bot, update):
        img_req = update.callback_query.data
        await get_img(bot, update, req=img_req)

    async def generate_img(self, prompt):
        result = ''
        self.img_req_data['data']['prompt'] = prompt
        res = [url['url'] for url in json.loads(await req.post(img_req_data['url'], headers=img_req_data['header'], json=img_req_data['data']).text)['data']]
        for url in res:
            result += url
        return result

    def run(self):
        print('Bot is running...')

        updater.dispatcher.add_handler(CommandHandler('start', start))
        updater.dispatcher.add_handler(CommandHandler('help', help))
        updater.dispatcher.add_handler(CommandHandler('chat', chat))
        updater.dispatcher.add_handler(CommandHandler('refresh', refresh))
        updater.dispatcher.add_handler(CommandHandler('get_img', get_img))
        updater.dispatcher.add_handler(CallbackQueryHandler(regenerate))

        updater.start_polling()
        updater.idle()