import requests
import telebot
import xml.etree.ElementTree as ET

from telebot import custom_filters
from telebot import types

from telebot.states import State, StatesGroup
from telebot.states.sync.context import StateContext
from telebot.states.sync.middleware import StateMiddleware
from telebot.storage import StateMemoryStorage

# ---------------------------------------------------------
# НАСТРОЙКИ
# ---------------------------------------------------------

BOT_TOKEN = "8852272774:AAHz9_bqWjUTpDWB80HuzK8nSpMNsQy5c4M"

CBR_API_URL = "https://www.cbr.ru/scripts/XML_daily.asp"


# ---------------------------------------------------------
# СОЗДАНИЕ БОТА
# ---------------------------------------------------------

state_storage = StateMemoryStorage()

bot = telebot.TeleBot(
    BOT_TOKEN,
    state_storage=state_storage,
    use_class_middlewares=True,
)


# ---------------------------------------------------------
# СОСТОЯНИЯ
# ---------------------------------------------------------


class CurrencyStates(StatesGroup):
    waiting_for_currency = State()
    waiting_for_amount = State()


# ---------------------------------------------------------
# ДОСТУПНЫЕ ВАЛЮТЫ
# ---------------------------------------------------------

CURRENCIES = {
    "🇺🇸 Доллар": {
        "code": "USD",
        "name": "долларов",
        "symbol": "$",
    },
    "🇪🇺 Евро": {
        "code": "EUR",
        "name": "евро",
        "symbol": "€",
    },
    "🇨🇳 Юань": {
        "code": "CNY",
        "name": "юаней",
        "symbol": "¥",
    },
}


# ---------------------------------------------------------
# КЛАВИАТУРЫ
# ---------------------------------------------------------


def create_main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    button = types.KeyboardButton("💱 Конвертировать рубли")

    keyboard.add(button)

    return keyboard


def create_currency_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.add(
        types.KeyboardButton("🇺🇸 Доллар"),
        types.KeyboardButton("🇪🇺 Евро"),
    )

    keyboard.add(types.KeyboardButton("🇨🇳 Юань"))

    keyboard.add(types.KeyboardButton("❌ Отмена"))

    return keyboard


def create_cancel_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.add(types.KeyboardButton("❌ Отмена"))

    return keyboard


# ---------------------------------------------------------
# ПОЛУЧЕНИЕ КУРСА ВАЛЮТЫ
# ---------------------------------------------------------


def get_currency_rate(currency_code):
    """
    Получает курс выбранной валюты
    с сайта Банка России.
    """

    response = requests.get(
        CBR_API_URL,
        timeout=10,
    )

    response.raise_for_status()

    root = ET.fromstring(response.content)

    rate_date = root.attrib.get("Date")

    for currency in root.findall("Valute"):
        char_code = currency.find("CharCode").text

        if char_code == currency_code:
            nominal_text = currency.find("Nominal").text
            value_text = currency.find("Value").text

            nominal = int(nominal_text)

            value = float(value_text.replace(",", "."))

            # Например:
            # 10 юаней стоят 110 рублей.
            #
            # Чтобы узнать стоимость одного юаня:
            # 110 / 10 = 11 рублей.
            rate_for_one = value / nominal

            return rate_for_one, rate_date

    return None, rate_date


# ---------------------------------------------------------
# КОМАНДА /start
# ---------------------------------------------------------


@bot.message_handler(commands=["start"])
def command_start_handler(
    message,
    state: StateContext,
):
    # Удаляем старое состояние пользователя.
    state.delete()

    output_text = (
        "Добро пожаловать в конвертер валют!\n\n"
        "Бот переводит рубли в доллары, "
        "евро или китайские юани.\n\n"
        "Нажмите кнопку ниже."
    )

    bot.send_message(
        message.chat.id,
        output_text,
        reply_markup=create_main_keyboard(),
    )


# ---------------------------------------------------------
# НАЖАТИЕ КНОПКИ «КОНВЕРТИРОВАТЬ»
# ---------------------------------------------------------


@bot.message_handler(func=lambda message: (message.text == "💱 Конвертировать рубли"))
def convert_button_handler(
    message,
    state: StateContext,
):
    # Переводим пользователя
    # в состояние выбора валюты.
    state.set(CurrencyStates.waiting_for_currency)

    bot.send_message(
        message.chat.id,
        "Выберите валюту:",
        reply_markup=create_currency_keyboard(),
    )


# ---------------------------------------------------------
# ОТМЕНА
# ---------------------------------------------------------


@bot.message_handler(
    state="*",
    commands=["cancel"],
)
@bot.message_handler(
    state="*",
    func=lambda message: (message.text == "❌ Отмена"),
)
def cancel_handler(
    message,
    state: StateContext,
):
    state.delete()

    bot.send_message(
        message.chat.id,
        "Действие отменено.",
        reply_markup=create_main_keyboard(),
    )


# ---------------------------------------------------------
# ВЫБОР ВАЛЮТЫ
# ---------------------------------------------------------


@bot.message_handler(
    state=CurrencyStates.waiting_for_currency,
    func=lambda message: (message.text in CURRENCIES),
)
def currency_handler(
    message,
    state: StateContext,
):
    currency = CURRENCIES[message.text]

    # Сохраняем код валюты
    # внутри состояния пользователя.
    state.add_data(
        currency_code=currency["code"],
        currency_name=currency["name"],
        currency_symbol=currency["symbol"],
    )

    # Переходим к следующему состоянию.
    state.set(CurrencyStates.waiting_for_amount)

    output_text = (
        f"Вы выбрали валюту: "
        f"{currency['code']}.\n\n"
        "Введите сумму в рублях.\n\n"
        "Например: 1000"
    )

    bot.send_message(
        message.chat.id,
        output_text,
        reply_markup=create_cancel_keyboard(),
    )


# ---------------------------------------------------------
# НЕПРАВИЛЬНЫЙ ВЫБОР ВАЛЮТЫ
# ---------------------------------------------------------


@bot.message_handler(
    state=CurrencyStates.waiting_for_currency,
)
def incorrect_currency_handler(message):
    bot.send_message(
        message.chat.id,
        "Пожалуйста, выберите валюту кнопкой.",
        reply_markup=create_currency_keyboard(),
    )


# ---------------------------------------------------------
# ВВОД СУММЫ В РУБЛЯХ
# ---------------------------------------------------------


@bot.message_handler(
    state=CurrencyStates.waiting_for_amount,
    content_types=["text"],
)
def amount_handler(
    message,
    state: StateContext,
):
    amount_text = message.text.strip()

    # Разрешаем вводить как 1000.50,
    # так и 1000,50.
    amount_text = amount_text.replace(",", ".")

    try:
        rubles = float(amount_text)

        if rubles <= 0:
            bot.send_message(message.chat.id, "Сумма должна быть больше нуля.")

            return

    except ValueError:
        bot.send_message(
            message.chat.id,
            "Введите сумму числом.\n\n" "Например: 1000",
        )

        return

    # Получаем сохранённую валюту.
    with state.data() as data:
        currency_code = data.get("currency_code")

        currency_name = data.get("currency_name")

        currency_symbol = data.get("currency_symbol")

    try:
        rate, rate_date = get_currency_rate(currency_code)

        if rate is None:
            bot.send_message(message.chat.id, "Не удалось найти выбранную валюту.")

            return

        # Переводим рубли в выбранную валюту.
        result = rubles / rate

        output_text = (
            f"💱 Результат конвертации\n\n"
            f"{rubles:.2f} ₽ = "
            f"{result:.2f} {currency_symbol}\n\n"
            f"Курс Банка России:\n"
            f"1 {currency_code} = "
            f"{rate:.4f} ₽\n\n"
            f"Дата курса: {rate_date}\n\n"
            f"Вы получили примерно "
            f"{result:.2f} {currency_name}."
        )

        # После успешного расчёта
        # удаляем состояние.
        state.delete()

        bot.send_message(
            message.chat.id,
            output_text,
            reply_markup=create_main_keyboard(),
        )

    except requests.RequestException:
        bot.send_message(
            message.chat.id,
            "Не удалось подключиться "
            "к сервису Банка России.\n"
            "Попробуйте ещё раз позже.",
        )

    except ET.ParseError:
        bot.send_message(
            message.chat.id,
            "Не удалось обработать данные " "Банка России.",
        )


# ---------------------------------------------------------
# ОСТАЛЬНЫЕ СООБЩЕНИЯ
# ---------------------------------------------------------


@bot.message_handler(
    func=lambda message: True,
    content_types=["text"],
)
def unknown_message_handler(message):
    bot.send_message(
        message.chat.id,
        "Нажмите кнопку " "«Конвертировать рубли».",
        reply_markup=create_main_keyboard(),
    )


# ---------------------------------------------------------
# ПОДКЛЮЧЕНИЕ СОСТОЯНИЙ
# ---------------------------------------------------------

bot.add_custom_filter(custom_filters.StateFilter(bot))

bot.setup_middleware(StateMiddleware(bot))


# ---------------------------------------------------------
# ЗАПУСК БОТА
# ---------------------------------------------------------

print("Бот-конвертер запущен")

bot.infinity_polling(skip_pending=True)
