# 8944249543:AAGOYVkP9FjxcbskJ7QHafmQ8tnGy_Mi4Bo
# @eight_test1_bot

import telebot
import random

bot = telebot.TeleBot("8944249543:AAGOYVkP9FjxcbskJ7QHafmQ8tnGy_Mi4Bo")

answers = [
    "Да, точно стоит попробовать.",
    "Лучше немного подождать.",
    "Сейчас хороший момент.",
    "Не торопись с решением.",
    "Скорее всего всё получится.",
    "Сначала подумай ещё раз.",
    "Ответ пока неясен.",
    "Сделай это сегодня.",
    "Лучше спроси позже.",
    "Доверься своей интуиции.",
]

history = []


@bot.message_handler(commands=["start"])
def command_start_handler(message):
    output_text = "Добро пожаловать в бота Шар восьмёрка.\nОн даст тебе ответы на все жизненные вопросы.\nНажми одну из кнопок ниже (Получить совет или Показать историю советов)"

    reply_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    reply_keyboard.add(telebot.types.KeyboardButton("Получить совет"))
    reply_keyboard.add(telebot.types.KeyboardButton("Показать историю советов"))

    bot.send_message(message.chat.id, output_text, reply_markup=reply_keyboard)


@bot.message_handler(func=lambda message: message.text == "Получить совет")
def message_get_advice_handler(message):
    output_text = random.choice(answers)

    history.append(output_text)

    bot.send_message(message.chat.id, output_text)


@bot.message_handler(func=lambda message: message.text == "Показать историю советов")
def message_get_advice_history_handler(message):
    output_text = ""

    if len(history) != 0:
        for advice in history:
            output_text += advice + "\n\n"
    else:
        output_text = "Ваша история советов пуста"

    bot.send_message(message.chat.id, output_text)


@bot.message_handler(commands=["clear"])
def command_clear_handler(message):
    output_text = "История советов успешно очищена. Спрашивайте новые советы"

    history.clear()

    bot.send_message(message.chat.id, output_text)


bot.infinity_polling()
