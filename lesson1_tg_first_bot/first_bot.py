# 8852272774:AAHz9_bqWjUTpDWB80HuzK8nSpMNsQy5c4M
# @guess_game_0107_bot

import telebot
import random

bot = telebot.TeleBot("8852272774:AAHz9_bqWjUTpDWB80HuzK8nSpMNsQy5c4M")

user_number = 0
comp_number = 0


@bot.message_handler(func=lambda message: True)
def process_all_text_messages(message):
    global user_number
    global comp_number

    input_text = message.text.lower()

    output_text = ""

    if input_text == "/start":
        comp_number = random.randint(1, 100)
        user_number = 0

        output_text = "я загадал число от 1 до 100. попробуй отгадай. введи число, котороя я загадал"
    else:
        user_number = int(input_text)

        if user_number < comp_number:
            output_text = "введи побольше"
        elif user_number > comp_number:
            output_text = "введи меньше"
        elif user_number == comp_number:
            output_text = "урааа! ты угадал. для новой игры введи /start"

    bot.send_message(message.chat.id, output_text)


bot.infinity_polling()
