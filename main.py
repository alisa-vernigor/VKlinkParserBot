import requests
import vk_api
import telegram
from telegram import InputMediaPhoto, InputMediaVideo, InputMedia
from telegram.ext import MessageHandler, Updater, Dispatcher, CommandHandler, Filters
from telegram.error import BadRequest
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
    try:
        urls = parser.parse_link(update.message.text)
        album = []
        for url, url_type in urls:
            if url_type == Parser.UrlType.VIDEO:
                album.append(InputMediaVideo(media=url))
            elif url_type == Parser.UrlType.PHOTO:
                album.append(InputMediaPhoto(media=url))
        context.bot.send_media_group(
            chat_id=update.message.chat_id, media=album)
    except BadRequest as e:
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="Telegram servers couldn't reach some "
                                 "of the files :(")
    except Exception as e:
        pass


start_handler = CommandHandler('start', start_help)
help_handler = CommandHandler('help', start_help)
links_handler = MessageHandler(
    filters=Filters.regex(r'(https://)?vk.com(.)*'),
    callback=links
)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(links_handler)

updater.start_polling()
