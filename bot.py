# -*- coding: utf-8 -*-
import telebot
from telebot import types
from datetime import datetime
import random
import re

# ============ НАСТРОЙКИ ============
TOKEN = '8916491035:AAFXUju6ngQ5uWEONyQTeT-StN3xZH0OIyw'
# ==================================

bot = telebot.TeleBot(TOKEN)

# ============ РАЗРАБОТЧИК ============
DEVELOPER = "@IKingTD"  # ← поменяй на свой ник

# ============ РАСПИСАНИЕ (можешь поменять) ============
SCHEDULE = {
    "Понедельник": ["Математика", "Русский", "Физика", "История"],
    "Вторник":     ["Английский", "Химия", "Физра", "Литература"],
    "Среда":       ["Математика", "Биология", "География", "Английский"],
    "Четверг":     ["Физика", "Математика", "Русский", "Физра"],
    "Пятница":     ["История", "Английский", "Химия", "Литература"],
    "Суббота":     ["Классный час"],
    "Воскресенье": ["Выходной 🎉"],
}

# ============ ПОГОДА (имитация) ============
WEATHER_STATES = ["☀️ Ясно", "⛅ Облачно", "🌧 Дождь", "❄️ Снег", "🌤 Переменно", "🌫 Туман"]

def get_weather(city):
    # Пока имитация — потом подключим API
    # Сделаем «погоду» зависящей от города — чтобы разные города давали разные числа
    seed = sum(ord(c) for c in city) + datetime.now().day
    random.seed(seed)
    temp = random.randint(-15, 32)
    state = random.choice(WEATHER_STATES)
    humidity = random.randint(30, 95)
    wind = random.randint(1, 15)
    random.seed()  # сброс
    return {"temp": temp, "state": state, "humidity": humidity, "wind": wind}

def advice_by_weather(temp):
    if temp < -10:
        return "🥶 Очень холодно! Пуховик, шапка, шарф, перчатки."
    if temp < 0:
        return "❄️ Морозно. Куртка, шапка, перчатки."
    if temp < 10:
        return "🧥 Прохладно. Куртка или толстовка."
    if temp < 20:
        return "👕 Тепло. Джинсы, футболка, лёгкая кофта."
    if temp < 27:
        return "😎 Жарко. Футболка и шорты."
    return "🔥 Очень жарко! Лёгкая одежда и вода с собой."

# ============ ВСПОМОГАТЕЛЬНОЕ ============
def get_schedule_for_day(day_name):
    return SCHEDULE.get(day_name, [])

def today_name():
    days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
    return days[datetime.now().weekday()]

# ============ ОБРАБОТЧИК КОМАНД С ТОЧКОЙ ============
# Регулярка ловит сообщения, начинающиеся с точки
COMMAND_PATTERN = re.compile(r'^\.(\S+)\s*(.*)', re.IGNORECASE)

# Список известных команд
COMMANDS = {
    'старт', 'start', 'хелп', 'help', 'помощь',
    'кто разраб', 'разраб', 'автор', 'кто создал',
    'сводка', 'погода', 'расписание', 'уроки', 'сегодня',
}

@bot.message_handler(func=lambda m: m.text and m.text.startswith('.'))
def handle_dot_command(message):
    match = COMMAND_PATTERN.match(message.text.strip())
    if not match:
        return

    cmd = match.group(1).lower()
    args = match.group(2).strip() if match.group(2) else ''

    chat_id = message.chat.id
    user_name = message.from_user.first_name or "друг"

    # --- .кто разраб ---
    if cmd in ['кто разраб', 'разраб', 'автор', 'кто создал']:
        text = (
            f"👨‍💻 <b>Разработчик этого бота</b>\n\n"
            f"Меня создал: <b>{DEVELOPER}</b>\n\n"
            f"💡 Бот умеет:\n"
            f"• ☀️ Делать утреннюю сводку\n"
            f"• 🌤 Показывать погоду\n"
            f"• 📚 Присылать расписание\n\n"
            f"📩 По вопросам — пиши разработчику."
        )
        bot.send_message(chat_id, text, parse_mode='HTML')
        return

    # --- .старт / .start ---
    if cmd in ['старт', 'start']:
        text = (
            f"👋 Привет, <b>{user_name}</b>!\n\n"
            f"Я — утренний бот-помощник.\n\n"
            f"📋 <b>Мои команды:</b>\n\n"
            f"<code>.кто разраб</code> — об авторе\n"
            f"<code>.сводка Москва</code> — сводка на день\n"
            f"<code>.погода Казань</code> — погода в городе\n"
            f"<code>.расписание</code> — расписание уроков\n"
            f"<code>.хелп</code> — эта справка\n\n"
            f"💡 Можно писать как в личке, так и в группе!"
        )
        bot.send_message(chat_id, text, parse_mode='HTML')
        return

    # --- .хелп / .help ---
    if cmd in ['хелп', 'help', 'помощь']:
        text = (
            "📖 <b>Список команд:</b>\n\n"
            "<code>.кто разраб</code> — информация о разработчике\n"
            "<code>.сводка [город]</code> — утренняя сводка\n"
            "<code>.погода [город]</code> — погода в городе\n"
            "<code>.расписание</code> — уроки на сегодня\n"
            "<code>.сегодня</code> — что сегодня\n"
            "<code>.хелп</code> — эта справка\n\n"
            "💡 <b>Примеры:</b>\n"
            "<code>.сводка Москва</code>\n"
            "<code>.погода Санкт-Петербург</code>\n"
            "<code>.сводка Алматы</code>"
        )
        bot.send_message(chat_id, text, parse_mode='HTML')
        return

    # --- .сводка [город] ---
    if cmd in ['сводка', 'сегодня']:
        city = args if args else 'Москва'
        w = get_weather(city)
        day = today_name()
        lessons = get_schedule_for_day(day)
        date_str = datetime.now().strftime('%d.%m.%Y')

        text = (
            f"☀️ <b>Доброе утро, {user_name}!</b>\n"
            f"📅 {date_str}, {day}\n\n"
            f"🌍 <b>Город:</b> {city}\n"
            f"🌡 <b>Погода:</b> {w['temp']}°C, {w['state']}\n"
            f"💧 Влажность: {w['humidity']}% · 💨 Ветер: {w['wind']} м/с\n\n"
            f"👕 <b>Что надеть:</b>\n{advice_by_weather(w['temp'])}\n\n"
        )

        if lessons:
            text += f"📚 <b>Уроков сегодня: {len(lessons)}</b>\n"
            for i, lesson in enumerate(lessons[:5], 1):
                text += f"{i}. {lesson}\n"
            if len(lessons) > 5:
                text += f"...и ещё {len(lessons) - 5}\n"
        else:
            text += "🎉 <b>Уроков нет — отдыхай!</b>\n"

        text += f"\n💪 <i>Хорошего дня!</i>"
        bot.send_message(chat_id, text, parse_mode='HTML')
        return

    # --- .погода [город] ---
    if cmd == 'погода':
        city = args if args else 'Москва'
        w = get_weather(city)
        text = (
            f"🌤 <b>Погода в городе {city}</b>\n\n"
            f"🌡 Температура: <b>{w['temp']}°C</b>\n"
            f"☁️ {w['state']}\n"
            f"💧 Влажность: {w['humidity']}%\n"
            f"💨 Ветер: {w['wind']} м/с\n\n"
            f"👕 <b>Что надеть:</b>\n{advice_by_weather(w['temp'])}"
        )
        bot.send_message(chat_id, text, parse_mode='HTML')
        return

    # --- .расписание / .уроки ---
    if cmd in ['расписание', 'уроки']:
        day = today_name()
        lessons = get_schedule_for_day(day)
        text = f"📚 <b>Расписание на {day}:</b>\n\n"
        if lessons:
            for i, lesson in enumerate(lessons, 1):
                text += f"{i}. {lesson}\n"
        else:
            text += "Уроков нет 🎉"
        bot.send_message(chat_id, text, parse_mode='HTML')
        return

    # --- неизвестная команда ---
    bot.send_message(
        chat_id,
        f"🤔 Неизвестная команда: <code>.{cmd}</code>\n\n"
        f"Напиши <code>.хелп</code> чтобы увидеть список.",
        parse_mode='HTML'
    )

# ============ ОБРАБОТКА ОБЫЧНЫХ СООБЩЕНИЙ (в личке) ============
@bot.message_handler(commands=['start'])
def cmd_start(message):
    user_name = message.from_user.first_name or "друг"
    text = (
        f"👋 Привет, <b>{user_name}</b>!\n\n"
        f"Я работаю по командам <b>с точкой</b> в начале.\n\n"
        f"Напиши <code>.хелп</code> чтобы увидеть все команды."
    )
    bot.send_message(message.chat.id, text, parse_mode='HTML')

@bot.message_handler(func=lambda m: m.chat.type == 'private' and m.text and not m.text.startswith('.'))
def fallback_private(message):
    bot.send_message(
        message.chat.id,
        "🤔 Я работаю только по командам с точкой.\n\n"
        "Напиши <code>.хелп</code> чтобы увидеть список.",
        parse_mode='HTML'
    )

# ============ ЗАПУСК ============
if __name__ == '__main__':
    print("🤖 Бот запущен...")
    print(f"👨‍💻 Разработчик: {DEVELOPER}")
    bot.infinity_polling()
