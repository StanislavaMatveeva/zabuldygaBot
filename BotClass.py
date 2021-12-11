from telebot.types import File, Message, MessageAutoDeleteTimerChanged, Sticker, StickerSet
import random
import pyowm
from textblob import TextBlob
import BotEnum

class BotClass:

    def __init__(self, bot, message, helpData):
        self.bot = bot
        self.message = message
        self.helpData = helpData

    def greetings(self, text):
        triggerFrases = self.helpData['trigger_frases']
        frases = self.helpData['frases']
        reactions = self.helpData['reactions']
        botEnum = BotEnum.BotEnum()
        if triggerFrases[botEnum.HELLO] in text.lower() and triggerFrases[botEnum.HOW_ARE_YOU] in text.lower():
            answer = frases[botEnum.HELLO] + '. ' + frases[botEnum.ALL_IS_OKEY]
        elif triggerFrases[botEnum.HOW_ARE_YOU] in text.lower():
            answer = frases[botEnum.ALL_IS_OKEY]
        elif triggerFrases[botEnum.HELLO] in text.lower():
            answer = frases[botEnum.HELLO]
        elif triggerFrases[botEnum.POLITE_HELLO] in text.lower():
            answer = frases[botEnum.FUNNY_HELLO]
        elif triggerFrases[botEnum.THANK_YOU] in text.lower() or triggerFrases[botEnum.POLITE_THANK_YOU] in text.lower():
            answer = frases[botEnum.NOT_AT_ALL]
        elif triggerFrases[botEnum.NIGTH] in text.lower() or triggerFrases[botEnum.SLEEP] in text.lower() or triggerFrases[botEnum.DREAM] in text.lower():
            answer = frases[botEnum.GOOD_NIGHT] 
        elif triggerFrases[botEnum.GOOD] in text.lower():
            if triggerFrases[botEnum.MORNING] in text.lower():
                answer = frases[botEnum.GOOD_MORNING]
            elif triggerFrases[botEnum.DAY] in text.lower():
                answer = frases[botEnum.FUNNY_HELLO]
        elif triggerFrases[botEnum.SAD] in text.lower() or triggerFrases[botEnum.BAD] in text.lower():  
            answer = frases[botEnum.WHAT_HAPPEND]
        elif triggerFrases[botEnum.BOT_START] == text.lower():
            answer = frases[botEnum.FUNNY_HELLO] + '. ' + frases[botEnum.WHAT_DO_YOU_NEED]
            answer += '\n'
            answer += self.helpData['help'][0]
        elif triggerFrases[botEnum.BOT_HELP] == text.lower():
            answer = frases[botEnum.HELP]
            answer += '\n'
            answer += self.helpData['help'][0]
        elif triggerFrases[botEnum.BYE] in text.lower():
            answer = frases[botEnum.GOODBYE]
        elif triggerFrases[botEnum.WEATHER] in text.lower() or triggerFrases[botEnum.FORECAST] in text.lower():
            answer = self.getWeather()
        elif triggerFrases[botEnum.ANECDOTE] in text.lower():
            answer = random.choice(self.helpData['anecdotes'])
        elif triggerFrases[botEnum.JOKE] in text.lower() or triggerFrases[botEnum.FUN] in text.lower():
            answer = random.choice(self.helpData['jokes'])
        else:
            answer = random.choice(reactions)
        return answer

    def getWeather(self):
        owm = pyowm.OWM(self.helpData['tokens'][0]['owm_token'])
        botEnum = BotEnum.BotEnum()
        city = self.helpData['yandex_data'][botEnum.CITY]
        latitude = self.helpData['yandex_data'][botEnum.LATITUDE]
        longitude = self.helpData['yandex_data'][botEnum.LONGITUDE]
        w = owm.weather_manager().weather_at_place(city).weather
        blob = TextBlob(w.detailed_status).translate(to = 'ru')
        text = ['Погода в Москве сейчас:\n', str(blob),
        '\nТемпература: min: ', str(w.temperature('celsius')['temp_min']), ' C, '
        'max: ', str(w.temperature('celsius')['temp_max']), ' C'
        '\nСкорость ветра: ', str(w.wind(unit = 'miles_hour')['speed']), ' m/h'
        '\nДавление: ', str(w.pressure['press']), ' hPa'
        '\nРассвет: ', str(w.sunrise_time('date')),
        '\nЗакат: ', str(w.sunset_time('date')),
        '\n', '\nПрогноз на завтра:\n']
        answer = str()
        for t in text:
            answer += str(t)
        answer += f'\nhttps://yandex.ru/pogoda/{city}?lat={latitude}&lon={longitude}'
        return answer

    def working(self):
        text = self.message.text
        frases = self.helpData['frases']
        stickerPack = self.helpData['stickers']
        randomSticker = random.choice(stickerPack)
        botEnum = BotEnum.BotEnum()
        if self.message.content_type == 'text':
            answer = self.greetings(text)
            self.bot.send_message(self.message.chat.id, answer)
        elif self.message.content_type == 'sticker':
            self.bot.send_sticker(self.message.chat.id, randomSticker)
        elif self.message.content_type == 'audio' or self.message.content_type == 'photo' or self.message.content_type == 'video':
            self.bot.send_sticker(self.message.chat.id, randomSticker)
        else:
            self.bot.send_message(self.message.chat.id, frases[botEnum.MISUNDERSTANDING])
            self.bot.send_message(self.message.chat.id, self.helpData['help'][0])
            