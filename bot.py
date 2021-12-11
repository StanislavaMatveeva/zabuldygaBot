import telebot
from telebot.types import MessageAutoDeleteTimerChanged, StickerSet
import BotClass
import json


with open('helpData.json', 'r') as read_file:
    helpData = json.load(read_file)

bot = telebot.TeleBot(helpData['tokens'][0]['bot_token'])

@bot.message_handler(content_types = ['text', 'photo', 'audio', 'video', 'sticker'])
def getMessage(message):
    botClass = BotClass.BotClass(bot, message, helpData)
    botClass.working()

bot.polling(non_stop = True, interval = 0)