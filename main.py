import requests
import vk_api
import telegram
from telegram.ext import MessageHandler, Updater, Dispatcher, CommandHandler, Filters
from settings import service_key, test_id, token
from my_parser import Parser
import os

updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher
parser = Parser(service_key)

def start_help(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text='По всем вопросам обращаться к @sphericalpotatoinvacuum или @allisyonok'
    )

def links(update, context):
    print("I am in links")
    path = parser.make_directory()
    try:
        parser.parse_link(update.message.text, path)
        for f in os.listdir(path):
            print(f)
            if f[-1] == "4":
                print("here")
                context.bot.send_video(chat_id=update.message.chat_id, video=open(f"{path}\\{f}", 'rb'), timeout=40)
    except Exception as e:
        pass
    parser.delete_directory(path)


start_handler = CommandHandler('start', start_help)
help_handler = CommandHandler('help', start_help)
links_handler = MessageHandler(filters=Filters.text, callback=links)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(links_handler)

updater.start_polling()
