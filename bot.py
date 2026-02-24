import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

TOKEN = "8795585040:AAFUoPPA92H01xFLbHuRY4h_1bsirwDPSvU"
WEBAPP_URL = "https://ТУТ_БУДЕ_RENDER_URL/web/index.html"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🚀 Open AI Signal App",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )
        ]
    ])

    await message.answer("Open AI Signal Pro:", reply_markup=kb)

async def main():
    print("Bot started...")
    await dp.start_polling(bot)

if name == "__main__":
    asyncio.run(main())