import requests
import telebot

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

GEOCODING_API_URL = "https://geocoding-api.open-meteo.com/v1/search"

WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"


# ---------------------------------------------------------
# СОЗДАНИЕ БОТА И ХРАНИЛИЩА СОСТОЯНИЙ
# ---------------------------------------------------------

state_storage = StateMemoryStorage()

bot = telebot.TeleBot(
    BOT_TOKEN,
    state_storage=state_storage,
    use_class_middlewares=True,
)


# ---------------------------------------------------------
# СОСТОЯНИЯ БОТА
# ---------------------------------------------------------


class WeatherStates(StatesGroup):
    waiting_for_city = State()


# ---------------------------------------------------------
# ОПИСАНИЯ КОДОВ ПОГОДЫ
# ---------------------------------------------------------

WEATHER_CODES = {
    0: "ясно ☀️",
    1: "преимущественно ясно 🌤",
    2: "переменная облачность ⛅",
    3: "пасмурно ☁️",
    45: "туман 🌫",
    48: "изморозь и туман 🌫",
    51: "слабая морось 🌦",
    53: "морось 🌦",
    55: "сильная морось 🌧",
    56: "слабая ледяная морось 🌧",
    57: "сильная ледяная морось 🌧",
    61: "слабый дождь 🌦",
    63: "дождь 🌧",
    65: "сильный дождь 🌧",
    66: "слабый ледяной дождь 🌧",
    67: "сильный ледяной дождь 🌧",
    71: "слабый снег 🌨",
    73: "снег 🌨",
    75: "сильный снег ❄️",
    77: "снежные зёрна ❄️",
    80: "слабый ливень 🌦",
    81: "ливень 🌧",
    82: "сильный ливень ⛈",
    85: "слабый снегопад 🌨",
    86: "сильный снегопад ❄️",
    95: "гроза ⛈",
    96: "гроза с градом ⛈",
    99: "сильная гроза с градом ⛈",
}


# ---------------------------------------------------------
# КЛАВИАТУРЫ
# ---------------------------------------------------------


def create_main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    weather_button = types.KeyboardButton("🌤 Узнать погоду")

    keyboard.add(weather_button)

    return keyboard


def create_cancel_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    cancel_button = types.KeyboardButton("❌ Отмена")

    keyboard.add(cancel_button)

    return keyboard


# ---------------------------------------------------------
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ---------------------------------------------------------


def find_city(city_name):
    """
    Ищет город через Geocoding API.

    Возвращает словарь с информацией о городе
    или None, если город не найден.
    """

    params = {
        "name": city_name,
        "count": 1,
        "language": "ru",
        "format": "json",
    }

    response = requests.get(
        GEOCODING_API_URL,
        params=params,
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()

    results = data.get("results")

    if not results:
        return None

    return results[0]


def get_current_weather(latitude, longitude):
    """
    Получает текущую погоду по координатам.
    """

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "temperature_2m,"
            "apparent_temperature,"
            "relative_humidity_2m,"
            "weather_code,"
            "wind_speed_10m"
        ),
        "timezone": "auto",
    }

    response = requests.get(
        WEATHER_API_URL,
        params=params,
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()

    return data["current"]


def get_weather_description(weather_code):
    """
    Превращает числовой код погоды
    в понятное описание.
    """

    return WEATHER_CODES.get(
        weather_code,
        "неизвестное состояние погоды",
    )


def format_temperature(temperature):
    """
    Добавляет плюс перед положительной температурой.
    """

    if temperature > 0:
        return f"+{temperature}"

    return str(temperature)


def create_location_name(city):
    """
    Собирает красивое название места:
    город, регион, страна.
    """

    location_parts = []

    city_name = city.get("name")
    region_name = city.get("admin1")
    country_name = city.get("country")

    if city_name:
        location_parts.append(city_name)

    if region_name and region_name != city_name:
        location_parts.append(region_name)

    if country_name:
        location_parts.append(country_name)

    return ", ".join(location_parts)


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
        "Добро пожаловать в погодного бота!\n\n"
        "Я могу показать текущую погоду "
        "в любом городе.\n\n"
        "Нажмите кнопку «Узнать погоду»."
    )

    bot.send_message(
        message.chat.id,
        output_text,
        reply_markup=create_main_keyboard(),
    )


# ---------------------------------------------------------
# НАЖАТИЕ КНОПКИ «УЗНАТЬ ПОГОДУ»
# ---------------------------------------------------------


@bot.message_handler(func=lambda message: (message.text == "🌤 Узнать погоду"))
def weather_button_handler(
    message,
    state: StateContext,
):
    # Переводим пользователя в состояние
    # ожидания названия города.
    state.set(WeatherStates.waiting_for_city)

    output_text = (
        "Введите название города.\n\n" "Например:\n" "Брянск\n" "Москва\n" "Владивосток"
    )

    bot.send_message(
        message.chat.id,
        output_text,
        reply_markup=create_cancel_keyboard(),
    )


# ---------------------------------------------------------
# ОТМЕНА ДЕЙСТВИЯ
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
    # Удаляем текущее состояние.
    state.delete()

    bot.send_message(
        message.chat.id,
        "Действие отменено.",
        reply_markup=create_main_keyboard(),
    )


# ---------------------------------------------------------
# ПОЛУЧЕНИЕ НАЗВАНИЯ ГОРОДА
# ---------------------------------------------------------


@bot.message_handler(
    state=WeatherStates.waiting_for_city,
    content_types=["text"],
)
def city_handler(
    message,
    state: StateContext,
):
    city_name = message.text.strip()

    if len(city_name) < 2:
        bot.send_message(
            message.chat.id,
            "Название города слишком короткое. " "Попробуйте ещё раз.",
        )

        return

    try:
        # Ищем город.
        city = find_city(city_name)

        if city is None:
            bot.send_message(
                message.chat.id,
                "Я не смог найти такой город.\n\n"
                "Проверьте название и попробуйте ещё раз.",
            )

            return

        latitude = city["latitude"]
        longitude = city["longitude"]

        # Получаем текущую погоду.
        weather = get_current_weather(
            latitude,
            longitude,
        )

        temperature = weather["temperature_2m"]

        apparent_temperature = weather["apparent_temperature"]

        humidity = weather["relative_humidity_2m"]

        wind_speed = weather["wind_speed_10m"]

        weather_code = weather["weather_code"]

        description = get_weather_description(weather_code)

        location_name = create_location_name(city)

        output_text = (
            f"🌍 Погода: {location_name}\n\n"
            f"🌡 Температура: "
            f"{format_temperature(temperature)} °C\n"
            f"🤔 Ощущается как: "
            f"{format_temperature(apparent_temperature)} °C\n"
            f"💧 Влажность: {humidity}%\n"
            f"💨 Скорость ветра: {wind_speed} км/ч\n"
            f"🌤 Состояние: {description}"
        )

        # После успешного получения погоды
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
            "Не удалось подключиться к сервису погоды.\n"
            "Попробуйте ещё раз немного позже.",
        )

    except KeyError:
        bot.send_message(
            message.chat.id,
            "Сервис погоды вернул неполные данные.\n"
            "Попробуйте выбрать другой город.",
        )


# ---------------------------------------------------------
# ОБРАБОТЧИК ОСТАЛЬНЫХ СООБЩЕНИЙ
# ---------------------------------------------------------


@bot.message_handler(
    func=lambda message: True,
    content_types=["text"],
)
def unknown_message_handler(message):
    output_text = "Я не понимаю эту команду.\n\n" "Нажмите кнопку «Узнать погоду»."

    bot.send_message(
        message.chat.id,
        output_text,
        reply_markup=create_main_keyboard(),
    )


# ---------------------------------------------------------
# ПОДКЛЮЧЕНИЕ STATE
# ---------------------------------------------------------

# Фильтр позволяет писать в обработчике:
# state=WeatherStates.waiting_for_city
bot.add_custom_filter(custom_filters.StateFilter(bot))

# Middleware передаёт StateContext
# в функции обработчиков.
bot.setup_middleware(StateMiddleware(bot))


# ---------------------------------------------------------
# ЗАПУСК БОТА
# ---------------------------------------------------------

print("Погодный бот запущен")

bot.infinity_polling(skip_pending=True)
