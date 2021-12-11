from telebot.types import KeyboardButton, ReplyKeyboardMarkup
import BotEnum
import random

class BotKeys:

    def __init__(self, message, helpData):
        self.message = message
        self.helpData = helpData

    def initKeyboard(self):
        buttonHi = KeyboardButton('привет')
        buttonAnecdot = KeyboardButton('анекдот')
        buttonJoke = KeyboardButton('цитата')
        buttonWeather = KeyboardButton('погода')
        buttonHelp = KeyboardButton('помощь')
        buttonBye = KeyboardButton('пока')
        botKeyboard = ReplyKeyboardMarkup(resize_keyboard = True)
        botKeyboard.add(buttonHi)
        botKeyboard.add(buttonAnecdot)
        botKeyboard.add(buttonJoke)
        botKeyboard.add(buttonWeather)
        botKeyboard.add(buttonHelp)
        botKeyboard.add(buttonBye)
        return botKeyboard

    async def working(self):
        botEnum = BotEnum.BotEnum()
        botKeyboard = self.initKeyboard()
        frases = self.helpData['frases']
        await self.message.reply(frases[botEnum.HELLO], reply_markup = botKeyboard)
        # elif self.botClass.message.commands == 'anecdote':
        #     self.botClass.message.reply(random.choice(self.botClass.helpData['anecdotes']), reply_markup = botKeyboard)
        # elif self.botClass.message.commands == 'joke':
        #     self.botClass.message.reply(random.choice(self.botClass.helpData['jokes']), reply_markup = botKeyboard)
        # elif self.botClass.message.commands == 'weather':
        #     self.botClass.message.reply(self.botClass.getWeather(), reply_markup = botKeyboard)
        # elif self.botClass.message.commands == 'help':
        #     answer = frases[botEnum.HELP]
        #     answer += '\n'
        #     answer += self.botClass.helpData['help'][0]
        #     self.botClass.message.reply(answer, reply_markup = botKeyboard)
        # elif self.botClass.message.commands == 'bye':
        #     self.botClass.message.reply(frases[botEnum.GOODBYE], reply_markup = botKeyboard)
    