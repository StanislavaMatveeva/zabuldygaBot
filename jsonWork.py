import json
from os import SEEK_END, read
import random
from geopy import geocoders

# start = input('write something to start\n')
# if start != None:
#     helpData = {}
#     helpData['tokens'] = []
#     helpData['tokens'].append({'bot_token': '5013707338:AAGYtVQ7SqptQ6qu47ZraNXhKh_fh3gaqJw',
#                             'yandex_token': 'ff8480b5-abcb-4fe1-89d9-c57b048cafa6'})
#     helpData['frases'] = []
#     helpData['reactions'] = []
#     helpData['stickers'] = []
#     helpData['anecdotes'] = []
#     helpData['jokes'] = []
#     helpData['yandex_data'] = []

#     print('add frases\n')
#     end = 1
#     i = 0
#     while end != 0:
#         fraseText = input('enter frase text\n')
#         print(f'{i}. i got {fraseText}\n')
#         helpData['frases'].append(fraseText)
#         i += 1
#         end = int(input('enter end\n'))
#     print('end of adding\n')

#     print('\nadd reactions\n')
#     end = 1
#     i = 0
#     while end != 0:
#         reactText = input('enter reaction text\n')
#         print(f'{i}. i got {reactText}\n')
#         helpData['reactions'].append(reactText)
#         i += 1
#         end = int(input('enter end\n'))
#     print('end of adding\n')

#     stickersFile = open('stickers.txt', 'r')
#     lines = stickersFile.readlines()
#     stickersFile.close()
#     for line in lines:
#         helpData['stickers'].append(line)

#     anecdotesFile = open('anecdotes.txt', 'r', encoding = 'utf-8')
#     lines = anecdotesFile.readlines()
#     anecdotesFile.close()
#     tmp = str()
#     for line in lines:
#         tmp += line
#         if line == '\n':
#             helpData['anecdotes'].append(tmp)
#             tmp = ' '

#     jokesFile = open('jokes.txt', 'r', encoding = 'utf-8')
#     lines = jokesFile.readlines()
#     jokesFile.close()
#     tmp = str()
#     for line in lines:
#         tmp += line
#         if line == '\n':
#             helpData['jokes'].append(tmp)
#             tmp = ' '

# geolocator = geocoders.Nominatim(user_agent = 'telebot')
# latitude = str(geolocator.geocode('Moscow').latitude)
# longitude = str(geolocator.geocode('Moscow').longitude)
# helpData['yandex_data'].append('Moscow')
# helpData['yandex_data'].append(latitude)
# helpData['yandex_data'].append(longitude)

# with open('helpData.json', 'w') as write_file:
#     json.dump(helpData, write_file)

# read_file.seek(SEEK_END)
#     result['trigger_frases'] = []

#     print('add trigger frases\n')
#     end = 1
#     i = 0
#     while end != 0:
#         triggerFraseText = input('enter frase text\n')
#         print(f'{i}. i got {triggerFraseText}\n')
#         result['trigger_frases'].append(triggerFraseText)
#         i += 1
#         end = int(input('enter end\n'))
#     print('end of adding\n')
#     json.dump(result, read_file)

with open("helpData.json", "r+", encoding='utf-8') as read_file:
     data = json.load(read_file)
#     text = 'ключевые фразы:\n\"анекдот\" - расскажу анекдот\n\"погода\" или \"прогноз\" - расскажу о сотоянии погоды в Москве на данный момент и о прогнозе на завтра\n\"шутка\" или \"прикол\" - напишу одну из цитат уважаемых В.В. Кличко и В.С. Черномырдина\n'
#     data['help'] = []
#     data['help'].append(text)
     data['anecdotes'][0] = 'Хозяин: - Вам грибочков положить?\nГость: - Нет, спасибо, я грибы только собирать люблю.\nХозяин: - Как хотите, могу и по полу раскидать...'
     data['anecdotes'][4] = 'Идет корова по дачному поселку:\n- Молоко, сыр, сметана!\nНаконец, отчаявшись:\n- Молоко, сыр, сметана, говядина в конце концов!'
     json.dump(data, read_file)

