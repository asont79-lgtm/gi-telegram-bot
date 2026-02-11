import os
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(TOKEN)
dp = Dispatcher()

GI_DB = {
    "рис белый": 70,
    "рис бурый": 50,
    "гречка": 50,
    "овсянка": 55,
    "яблоко": 36,
    "банан": 51,
    "картофель": 85,
    "макароны": 50,
    "хлеб белый": 75,
    "хлеб цельнозерновой": 50
}

def gi_level(gi: int) -> str:
    if gi <= 55:
        return "низкий"
    if gi <= 69:
        return "средний"
    return "высокий"

@dp.message(Command("start"))
async def start(m: Message):
    await m.answer(
        "👋 Привет! Я бот-калькулятор гликемического индекса (ГИ).\n\n"
        "Напиши продукт, например: гречка, яблоко, рис белый\n\n"
        "Команды:\n"
        "/gi продукт — узнать ГИ\n"
        "/gn GI углеводы — ГН (пример: /gn 70 30)\n"
        "/help — помощь\n"
        "/site — сайт"
    )

@dp.message(Command("site"))
async def site(m: Message):
    await m.answer("🔗 https://diabet-prosto.ru")

@dp.message(Command("help"))
async def help_cmd(m: Message):
    await m.answer(
        "Как пользоваться:\n"
        "• Напиши продукт: гречка\n"
        "• Или /gi гречка\n"
        "• ГН: /gn 70 30\n\n"
        "ГН = (ГИ × углеводы) / 100"
    )

@dp.message(Command("gi"))
async def gi_cmd(m: Message):
    text = m.text.replace("/gi", "").strip().lower()
    if not text:
        await m.answer("Напиши: /gi гречка")
        return
    gi = GI_DB.get(text)
    if gi is None:
        await m.answer("Не нашёл продукт. Попробуй: рис белый, гречка, яблоко.")
        return
    await m.answer(f"📊 {text.title()}\nГИ: {gi} ({gi_level(gi)})")

@dp.message(Command("gn"))
async def gn_cmd(m: Message):
    parts = m.text.split()
    if len(parts) != 3:
        await m.answer("Формат: /gn GI углеводы\nПример: /gn 70 30")
        return
    try:
        gi = float(parts[1])
        carbs = float(parts[2])
    except ValueError:
        await m.answer("Нужно указать числа. Пример: /gn 70 30")
        return
    gn = (gi * carbs) / 100
    level = "низкая" if gn <= 10 else "средняя" if gn <= 19 else "высокая"
    await m.answer(f"🧮 ГН: {gn:.1f}\nУровень: {level}")

@dp.message(F.text)
async def any_text(m: Message):
    text = m.text.strip().lower()
    gi = GI_DB.get(text)
    if gi is None:
        await m.answer("Не нашёл. Пример: гречка / яблоко / рис белый. Или /help")
        return
    await m.answer(f"📊 {text.title()}\nГИ: {gi} ({gi_level(gi)})")

async def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN не задан в переменных окружения.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
