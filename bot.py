import telebot
import requests
import phonenumbers
from phonenumbers import carrier, timezone, geocoder

bot = telebot.TeleBot("8039861900:AAF2T_ZLgxgGzBkiDQM08wSZ7uxVo8w7bnI")

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🕵️ Бот активирован\n/info @username - поиск информации\n/phone +79991234567 - поиск по номеру")

@bot.message_handler(commands=['info'])
def info_search(message):
    try:
        target = message.text.split()[1].replace('@', '')
        user_info = f"""📋 Данные по @{target}:

• ID: сбор данных...
• Username: @{target}
• Соцсети: поиск..."""
        bot.send_message(message.chat.id, user_info)
    except:
        bot.send_message(message.chat.id, "Использование: /info @username")

@bot.message_handler(commands=['phone'])
def phone_search(message):
    try:
        phone = message.text.split()[1]
        parsed = phonenumbers.parse(phone, "RU")
        operator = carrier.name_for_number(parsed, "ru")
        region = geocoder.description_for_number(parsed, "ru")
        
        phone_info = f"""📞 Информация по номеру:
• Оператор: {operator}
• Регион: {region}"""
        bot.send_message(message.chat.id, phone_info)
    except:
        bot.send_message(message.chat.id, "Использование: /phone +79991234567")

bot.polling()
