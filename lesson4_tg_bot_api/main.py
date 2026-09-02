# 8390475720:AAFaU7eCYUY2-rE0pEnxXLGaWz92DPaJcFo
# @converter_valut_21_07_01_bot


import telebot

import requests
import xml.etree.ElementTree as ET

bot = telebot.TeleBot("8390475720:AAFaU7eCYUY2-rE0pEnxXLGaWz92DPaJcFo")

money = 0


def get_valute_course(valute_name):
    response = requests.get("https://www.cbr.ru/scripts/XML_daily.asp")

    root = ET.fromstring(response.content)

    valute_node = root.find(f".//Valute[CharCode='{valute_name}']")

    value_text = valute_node.find("Value").text

    value_float = float(value_text.replace(",", "."))

    return value_float


@bot.message_handler(commands=["start"])
def command_start_handler(message):
    output_text = "Добро пожаловать в бота Конвертер валют.\nВначале введите суммму в рублях (целое положительное число). Отправьте её. А после выберете в какую валюту её перевести."

    bot.send_message(message.chat.id, output_text)


@bot.message_handler(func=lambda message: message.text.isdigit() == True)
def message_input_money_handler(message):
    global money
    money = int(message.text)

    output_text = "Сумма успешно записана.\nТеперь выберите с помощью клавиатуры в какую валюту вы хотите рубли переверсти."

    reply_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    reply_keyboard.add(telebot.types.KeyboardButton("Из рублей в доллары"))
    reply_keyboard.add(telebot.types.KeyboardButton("Из рублей в евро"))
    reply_keyboard.add(telebot.types.KeyboardButton("Из рублей в юани"))

    bot.send_message(message.chat.id, output_text, reply_markup=reply_keyboard)


@bot.message_handler(func=lambda message: message.text == "Из рублей в доллары")
def message_rub_to_usd_handler(message):
    usd_course = get_valute_course("USD")

    usd = money / usd_course

    output_text = f"курс доллара на сегодня {usd_course:.2f} рублей за доллар\nза {money} рублей вы получите {usd:.2f} долларов"

    bot.send_message(message.chat.id, output_text)


@bot.message_handler(func=lambda message: message.text == "Из рублей в евро")
def message_rub_to_eur_handler(message):
    output_text = "message_rub_to_eur_handler"

    bot.send_message(message.chat.id, output_text)


@bot.message_handler(func=lambda message: message.text == "Из рублей в юани")
def message_rub_to_cny_handler(message):
    output_text = "message_rub_to_cny_handler"

    bot.send_message(message.chat.id, output_text)


bot.infinity_polling()
