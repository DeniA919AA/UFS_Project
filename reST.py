import pandas as pd
from aiogram import Bot, Dispatcher, Router
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, Message
from aiogram.filters import CommandStart
import asyncio
import argparse

# --- Начало заимствованного кода из книги aiogram ---
# Парсер для аргументов командной строки
# https://docs.python.org/3/library/argparse.html

parser = argparse.ArgumentParser(description="Телеграм-бот для управления файлами.")
parser.add_argument('--reiting', type=str, required=True, help='Путь к файлу с рейтингом бойцов.')
parser.add_argument('--schedule', type=str, required=True, help='Путь к файлу с расписанием боев.')
parser.add_argument('--events', type=str, required=True, help='Путь к файлу с последними событиями.')
parser.add_argument('--prognosis', type=str, required=True, help='Путь к файлу с прогнозом боев.')
parser.add_argument('--daniel', type=str, required=True, help='Путь к файлу с информацией о бойцах.')
args = parser.parse_args()
# --- Конец заимствованного кода ---

REITING_FILE = args.reiting
SCHEDULE_FILE = args.schedule
EVENTS_FILE = args.events
PROGNOSIS_FILE = args.prognosis
DANIEL_FILE = args.daniel

# Токен бота
TELEGRAM_TOKEN = '7244801651:AAGAYvL2rIm4tA0EvGtXF3HxW5OqoDSAK5g'

from_router = Router()

# --- Начало заимствованного кода из книги aiogram ---
# Код основан на примерах из учебника по aiogram:
# https://github.com/MasterGroosha/aiogram-3-guide?ysclid=m4n6yla9ch986070169

@from_router.message(CommandStart())
async def cmd_start(message: Message):
    """
    Обрабатывает команду `/start` и выводит пользователю клавиатуру с возможностью выбрать одно из действий:
    - Рейтинг бойцов
    - Расписание боев
    - Последние события
    - Прогноз боя
    - Информация о бойце

    :param message: Сообщение от пользователя.
    :type message: aiogram.types.Message
    """
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Рейтинг бойцов")],
            [KeyboardButton(text="Расписание боев")],
            [KeyboardButton(text="Последние события")],
            [KeyboardButton(text="Прогноз боя")],
            [KeyboardButton(text="Информация о бойце")],
        ],
        resize_keyboard=True
    )
    await message.answer("Выберите действие:", reply_markup=keyboard)

# --- Конец заимствованного кода ---

@from_router.message()
async def handle_button(message: Message):
    """
    Обрабатывает нажатие кнопок на клавиатуре и выводит соответствующую информацию из файлов:
    - Рейтинг бойцов
    - Расписание боев
    - Последние события
    - Прогноз боя
    - Информация о бойце

    :param message: Сообщение от пользователя.
    :type message: aiogram.types.Message
    """
    if message.text == "Рейтинг бойцов":
        try:
            df = pd.read_excel(REITING_FILE)
            if df.shape[1] >= 1:
                result = df.iloc[:, [0]].to_string(index=False, header=False)
                await message.answer(result)
        except Exception as e:
            await message.answer(f"Произошла ошибка при чтении файла: {e}")

    elif message.text == "Расписание боев":
        try:
            df = pd.read_excel(SCHEDULE_FILE)
            if df.shape[1] >= 1:
                result = df.iloc[:, [0]].to_string(index=False, header=False)
                await message.answer(result)
        except Exception as e:
            await message.answer(f"Произошла ошибка при чтении файла: {e}")
    
    elif message.text == "Последние события":
        try:
            df = pd.read_excel(EVENTS_FILE)
            if df.shape[1] >= 1:
                result = df.iloc[:, [0]].to_string(index=False, header=False)
                await message.answer(result)
        except Exception as e:
            await message.answer(f"Произошла ошибка при чтении файла: {e}")

    elif message.text == "Прогноз боя":
        try:
            df = pd.read_excel(PROGNOSIS_FILE)
            if df.shape[1] >= 1:
                result = df.iloc[:, [0]].to_string(index=False, header=False)
                await message.answer(result)
        except Exception as e:
            await message.answer(f"Произошла ошибка при чтении файла: {e}")

    elif message.text == "Информация о бойце":
        await message.answer("Введите имя бойца:")

    else:
        try:
            df = pd.read_excel(DANIEL_FILE)
            name = message.text.strip()  
            row = df[df.iloc[:, 0].str.contains(name, case=False, na=False)]

            if not row.empty:
                victories = row.iloc[0, 2]
                losses = row.iloc[0, 3]
                height = row.iloc[0, 5]
                weight = row.iloc[0, 6]
                birthdate = row.iloc[0, 9]

                result = (
                    f"Информация о бойце {name}:\n"
                    f"Победы: {victories}\n"
                    f"Поражения: {losses}\n"
                    f"Рост: {height} см\n"
                    f"Вес: {weight} кг\n"
                    f"Дата рождения: {birthdate.strftime('%d-%m-%Y') if pd.notnull(birthdate) else 'Не указана'}"
                )
                await message.answer(result)
            else:
                await message.answer(f"Боец с именем '{name}' не найден в базе данных.")
        except Exception as e:
            await message.answer(f"Произошла ошибка при чтении файла 'Daniel.xlsx': {e}")

async def main():
    """
    Основная функция для запуска бота, которая инициализирует бота и начинает опрос сообщений.

    :returns: None
    :rtype: None
    """
    bot = Bot(token=TELEGRAM_TOKEN)
    dp = Dispatcher()
    dp.include_router(from_router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
