import requests
import vk_api
import telegram
from telegram.ext import MessageHandler, Updater, Dispatcher, CommandHandler, Filters
from settings import service_key, test_id, token

updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher

def start_help(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text='По всем вопросам обращаться к @sphericalpotatoinvacuum или @allisyonok'
    )

def echo(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
    text=update.message.text)


start_handler = CommandHandler('start', start_help)
help_handler = CommandHandler('help', start_help)
echo_handler = MessageHandler(filters=Filters.text, callback=echo)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(echo_handler)

updater.start_polling()

'''vk_session = vk_api.VkApi(token=service_key)
vk = vk_session.get_api()

obj = vk.wall.getById(posts=f"-{test_id}", fields="attachments")
print(obj[0]["attachments"][0]["photo"]["sizes"][-1]["url"])
with open("img.jpg", "wb") as f:
    img = requests.get(url=obj[0]["attachments"][0]["photo"]["sizes"][-1]["url"])
    f.write(img.content)'''


