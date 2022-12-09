from telegram_bot import TelegramBot
from dotenv import load_dotenv
from revChatGPT.revChatGPT import Chatbot
import os



def main():
    load_dotenv()

    required_values = ['TELEGRAM_BOT_TOKEN', 'OPENAI_EMAIL', 'OPENAI_PASSWORD']
    missing_values = [value for value in required_values if os.environ.get(value) is None]

    

    ai_config = {
        'authorization': os.getenv('OPENAI_AUTH_KEY')
    }

    telegram_config = {
        'telegram_token': os.getenv('TELEGRAM_BOT_TOKEN'),
        'allowed_users': os.getenv('ALLOWED_USERS', '*'),
        'api_key': os.getenv('OPENAI_API_KEY')
    }
    
    chat = Chatbot(ai_config, conversation_id=None)
    bot = TelegramBot(telegram_config, chat)
    bot.run()

if __name__=='__main__':
    main()