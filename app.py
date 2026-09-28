import logging
import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from config import settings
from db import engine, Base

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=settings.TELEGRAM_TOKEN)
dp = Dispatcher()

# Main reply keyboard
main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='🍏 Профиль'), KeyboardButton(text='🥗 Добавить приём пищи')],
        [KeyboardButton(text='⚙️ Настройки'), KeyboardButton(text='📊 Статистика')]
    ],
    resize_keyboard=True
)

@dp.message(Command(commands=['start']))
async def cmd_start(message: types.Message):
    # Create DB tables if not exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # Send welcome message
    await message.answer(
        f"Привет, {message.from_user.full_name}! Я твой помощник по учету калорий. Выбери действие:",
        reply_markup=main_kb
    )

@dp.message(lambda msg: msg.text == '🍏 Профиль')
async def show_profile(message: types.Message):
    # TODO: load user data and display
    await message.answer("Здесь будет твой профиль (вес, цель, TDEE, съедено сегодня)")

@dp.message(lambda msg: msg.text == '🥗 Добавить приём пищи')
async def add_meal(message: types.Message):
    # TODO: начать FSM для добавления приема пищи
    await message.answer("Введите название продукта или блюда:")

@dp.message(lambda msg: msg.text == '⚙️ Настройки')
async def settings_handler(message: types.Message):
    # TODO: изменить параметры пользователя
    await message.answer("Настройки: изменить вес, цель и т.д.")

@dp.message(lambda msg: msg.text == '📊 Статистика')
async def stats_handler(message: types.Message):
    # TODO: показать статистику
    await message.answer("Здесь будет статистика потребленных калорий за неделю")

@dp.message()
async def fallback(message: types.Message):
    await message.answer("Не понял команду. Пожалуйста, выбери из меню.", reply_markup=main_kb)

async def main():
    try:
        logger.info("Запуск бота...")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())