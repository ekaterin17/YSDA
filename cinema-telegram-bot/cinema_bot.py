from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from src.cinema import Cinema
from src.keys import keys
from src import message as msg

bot = Bot(token=keys["BOT_TOKEN"])
dp = Dispatcher(bot)

cinema = Cinema()


@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message) -> None:
    await bot.send_message(message.chat.id, msg.START_MSG)


@dp.message_handler(commands=["help"])
async def send_help(message: types.Message) -> None:
    await bot.send_message(message.chat.id, msg.HELP_MSG)


@dp.message_handler()
async def get_info(message: types.Message) -> None:
    movie_title = message.text
    info = await cinema.search(movie_title)
    await bot.send_message(message.chat.id, text=info)


if __name__ == '__main__':
    executor.start_polling(dp)
