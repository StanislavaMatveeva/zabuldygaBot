from contextlib import nullcontext
from os import linesep
from geopy.geocoders import yandex
from pyowm.constants import LANGUAGES
from pyowm.utils import timestamps
from pyowm.weatherapi25 import weather
from pyowm.weatherapi25.weather_manager import WeatherManager
from telebot.types import File, Message, MessageAutoDeleteTimerChanged, Sticker, StickerSet
import random
import pyowm
from geopy import geocoders
from textblob import TextBlob
import json

class BotClass:

    HELLO_ID = 0
    ALL_IS_OKEY_ID = 1
    HELP = 2
    WHAT_DO_YOU_NEED = 3
    MISUNDERSTANDING = 4

    stickerFileName = 'stickers.txt'
    jokesFileName = 'jokes.txt'
    frasesFileName = 'frases.txt'
    yandexToken = 'ff8480b5-abcb-4fe1-89d9-c57b048cafa6'
    latitude = ''
    longitude = ''
    city = 'moscow'
    
    frases = ['привет, родной', 'все путем. как сам?', 
        'чем могу помочь?', 'чем обязан?', 'наверное не понял...',
        'жееееесть ого', 'ГОООООЛ', 'круууууть',
         'ЛАДНО', 'вот этта да', 'ОГО', 'во делаааа', 'лол чтоооо']

    def __init__(self, bot, message):
        self.bot = bot
        self.message = message

    def getStickerPack(self):
        file = open(BotClass.stickerFileName, 'r')
        stickerPack = file.readlines()
        file.close()
        stickerPack = self.deleteLinesDiveders(stickerPack)
        return stickerPack

    def getJokes(self):
        file = open(BotClass.jokesFileName, 'r', encoding = 'utf-8')
        lines = file.readlines()
        file.close()
        jokes = list()
        tmp = str()
        for line in lines:
            tmp += line
            if line == '\n':
                jokes.append(tmp)
                tmp = ' '
        return jokes

    def getRandomJokeText(self):
        text = self.getJokes()
        joke = text[random.randint(0, len(text) - 1)]
        return str(joke)    
    
    def deleteLinesDiveders(self, lines):
        for i in range(len(lines)):
            if '\n' in lines[i]:
                lines[i] = lines[i].replace('\n', '')
        return lines

    def addStickerToStickerPack(self, sticker, stickerPack):
        file = open(BotClass.stickerFileName, 'a')
        if '\n' in sticker:
            sticker = sticker.replace('\n', '')
        stickerPack.append(sticker)
        file.write(sticker)
        file.close()
        return stickerPack

    def greetings(self, text):
        if 'как дела' in text.lower() and 'привет' in text.lower():
            answer = BotClass.frases[BotClass.HELLO_ID] + ' .' + BotClass.frases[BotClass.ALL_IS_OKEY_ID]
        elif 'как дела'in text.lower():
            answer = BotClass.frases[BotClass.ALL_IS_OKEY_ID]
        elif 'привет' in text.lower():
            answer = BotClass.frases[BotClass.HELLO_ID]
        elif text.lower() == '/start':
            answer = BotClass.frases[BotClass.HELLO_ID] + ' .' + BotClass.frases[BotClass.WHAT_DO_YOU_NEED]
        elif text.lower() == '/help':
            answer = BotClass.frases[BotClass.HELP]
        elif 'погод' in text.lower() or 'прогноз' in text.lower():
            answer = self.getWeather()
            self.getCoordinates()
            answer += f'\nhttps://yandex.ru/pogoda/{BotClass.city}?lat={BotClass.latitude}&lon={BotClass.longitude}'
        elif 'анекдот' in text.lower():
            answer = self.getRandomJokeText()
        elif '?' not in text:
            answer = BotClass.frases[random.randint(BotClass.WHAT_DO_YOU_NEED + 1, len(BotClass.frases) - 1)]
        else:
            answer = BotClass.frases[BotClass.MISUNDERSTANDING]
        return answer
    
    def getCoordinates(self):
        geolocator = geocoders.Nominatim(user_agent = 'telebot')
        BotClass.latitude = str(geolocator.geocode(BotClass.city).latitude)
        BotClass.longitude = str(geolocator.geocode(BotClass.city).longitude)

    def getWeather(self):
        owm = pyowm.OWM('8f657874630435aeeea03004973dda45')
        w = owm.weather_manager().weather_at_place(BotClass.city).weather
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
        return answer

    def working(self):
        text = self.message.text
        stickerPack = self.getStickerPack()
        randomSticker = random.choice(stickerPack)
        if self.message.content_type == 'text':
            answer = self.greetings(text)
            self.bot.send_message(self.message.chat.id, answer)
        elif self.message.content_type == 'sticker':
            sticker = self.message.sticker.file_id
            if sticker not in stickerPack:
                stickerPack = self.addStickerToStickerPack(sticker, stickerPack)
            self.bot.send_sticker(self.message.chat.id, randomSticker)
        elif self.message.content_type == 'audio' or self.message.content_type == 'photo' or self.message.content_type == 'video':
            self.bot.send_sticker(self.message.chat.id, randomSticker)
        else:
            self.bot.send_message(self.message.chat.id, BotClass.frases[BotClass.MISUNDERSTANDING])
            


# {'tokens': [{'bot_token': '5013707338:AAGYtVQ7SqptQ6qu47ZraNXhKh_fh3gaqJw', 
#             'yandex_token': 'ff8480b5-abcb-4fe1-89d9-c57b048cafa6'}], 
# 'frases': ['привет, родной', 'все путем. как сам?', 'чем могу помочь?', 'чем обязан?'], 
# 'reactions': ['наверное не понял...', 'жееееесть ого', 'ГОООООЛ', 'круууууть', 
#                 'ЛАДНО', 'вот этта да', 'ОГО', 'во делааааа', 'лол чтооооо'], 
# 'stickers': ['CAACAgIAAxkBAAICGmGxQdOFEumr9XVc3JUvkJzIvhyvAALqAQACHxS2CkjbR37qnfciIwQ\n', 
# 'CAACAgIAAxkBAAICG2GxQdS6Vg8H2FIM_3WrO1fPfd3rAAKVAwACP5XMCtwcJ-64p116IwQ\n', 'CAACAgIAAxkBAAICHGGxQdUKXkpxjU_pzviZlPKVW7rWAALvAAOWn4wO7uT5oQKY26IjBA\n', 'CAACAgIAAxkBAAICHWGxQda0hZOV2lRLd2ei6TTyzHP5AALwAQACHxS2CtsLU2PL-WHMIwQ\n', 'CAACAgIAAxkBAAICHmGxQddvQAhaNGzhxIBEhvfOaLocAAIhAgACHxS2CmIITT6DnbbGIwQ\n', 'CAACAgIAAxkBAAICH2GxQdfhsoT1LprXb3Ntymhge-iZAAIlAgACHxS2CotEtmFryhxeIwQ\n', 'CAACAgIAAxkBAAICIGGxQdh0VoGb9jjFcvlEtH9AdwGAAAI1AwACusCVBRZMmztTWNeIIwQ\n', 'CAACAgIAAxkBAAICIWGxQdk2dx0eiMSic1LX-InOieCdAAJ0AAPANk8T7D3m3XHZBqgjBA\n', 'CAACAgIAAxkBAAICImGxQdkWOjhsoPkMHZ2NNqga8iumAAKEAAOtWm4tfsZZRS5RrrUjBA\n', 'CAACAgIAAxkBAAICI2GxQdpLl-CZSrQhpr7LnFR0SSgOAAJCAwACusCVBfvFJAv1Cm6zIwQ\n', 
# 'CAACAgIAAxkBAAICJGGxQd2OE9JIAAEi_sH_3UJ5HHsp5wACIQIAAh8UtgpiCE0-g522xiME\n', 'CAACAgIAAxkBAAICJWGxQd09J0iPqRVsOIX40DXcDamVAALwAQACHxS2CtsLU2PL-WHMIwQ\n', 'CAACAgIAAxkBAAICJmGxQd5boKDSIbzR9f15oUCRXRlTAALvAAOWn4wO7uT5oQKY26IjBA\n', 'CAACAgIAAxkBAAICJ2GxQd9Kf7NKanUiKAPmIVTnO9BpAAKVAwACP5XMCtwcJ-64p116IwQ\n', 'CAACAgIAAxkBAAICKGGxQd9XmshZZc6ceaz3wJ7lArEaAALqAQACHxS2CkjbR37qnfciIwQ\n', 'CAACAgIAAxkBAAICKWGxQeCgGiAGRFQ-0JBaPBYOXF1UAAJSAQACIjeOBDZdiFEh7OSQIwQ\n', 'CAACAgIAAxkBAAICKmGxQeFBuXzq7RpJdTjDBQABZUcL6wACXwADRsGjDr3c1RfDlorNIwQ\n', 'CAACAgIAAxkBAAICK2GxQeGBck4xJ3LEOKJwJzcuKpuvAAIWAAM0SUAe-SkkrZmJKcMjBA\n', 'CAACAgIAAxkBAAICLGGxQeJ4zroe16PY6yjx1XOzEdhBAAIeAAM0SUAedoO-2rsCw0gjBA\n', 'CAACAgIAAxkBAAICLWGxQeLyzAn5SR8277ToIiOAqS02AAI1AAOc_jIwiienHY5-hOgjBA\n', 'CAACAgIAAxkBAAICLmGxQeXt2AooMldLvEXaYXJfZtZXAAI4AAOc_jIwAAEGj5l1bq2IIwQ\n', 'CAACAgIAAxkBAAICL2GxQeVZtFoD3_WeiU4Kxx6CetgsAAJIAQACIjeOBP3b9pUDR1QuIwQ\n', 'CAACAgIAAxkBAAICMGGxQeb6gItB0sHLORVcVbVk48X_AAI-AAOc_jIwnjeSBhKuB2ojBA\n', 'CAACAgIAAxkBAAICMWGxQqxpUkaI6ii4EEycEOuWLn-lAAIhAgACHxS2CmIITT6DnbbGIwQ'], 
# 'anecdotes': ['Хозяин: - Вам грбочков положить?\nГость: - Нет, спасибо, я грибы только собирать люблю.\nХозяин: - Как хотите, могу и по полу раскидать...\n\n', ' Дизайнер 2D игр не видит в совей работе перспективы\n\n', ' К доктору приходит пациент:\n- Доктор, у меня проблема: меня все игнорируют!\n- Следующий\n\n', ' Колобок повесился\n\n', ' Идет корова по дачному поселку:\n- Молоко, сыр, сметана!\nНаконец, отчаявшись:\n- Молоко, сыр, сметана, говядина вконце концов!\n\n', ' Буратино утонул\n\n'], 
# 'jokes': ['«…хотели как лучше, а получилось как всегда» (с) В.С. Черномырдин\n\n', 
# ' «А сегодня в завтрашний день не все могут смотреть. Вернее, смотреть могут не только лишь все, мало кто может это делать» (с) В.В. Кличко\n\n', 
# ' «Мы выполнили все пункты: от А до Б» (с) В.С. Черномырдин\n\n', 
# ' «Чем старше человек, тем больше ему лет» (с) В.В. Кличко\n\n', 
# ' «Мы не можем делать никому, чтобы было в ущерб себе» (с) В.С. Черномырдин\n\n', ' «Я встречался с многими милиционерами, которые погибли, с людьми—демонстрантами, которые погибли; и все мне задают вопрос…» (с) В.В. Кличко\n\n', ' «Отродясь такого не было, и вот — опять!» (с) В.С. Черномырдин\n\n', ' «Если шарик лопнул, его уже не надуешь. Вернее надуешь, но другой» (с) В.В. Кличко\n\n', ' «Курс у нас один — правильный» (с) В.С. Черномырдин\n\n', ' «Уже завтра, сегодня 
# станет вчера» (с) В.В. Кличко\n\n', ' «Лучше быть головой мухи, чем жопой слона» (с) В.С. Черномырдин\n\n', ' «Один в поле не двое» (с) В.В. Кличко\n\n'], 
# 'yandex_data': ['Moscow', '55.7504461', '37.6174943'], 
# 'trigger_frases': ['привет', 'как дела', 'здравствуй', '/start', '/help', 'погод', 'прогноз', 'анекдот', 'шутк', 
# 'прикол', 'добр', 'утр', 'день', 'ноч', 'снов', 'спать']}            