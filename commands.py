import random
from aiogram import types
import view, model
from bot import bot

async def start_game(message: types.Message):
    await model.set_game()
    await view.start_game(message)
    name = message.from_user.first_name
    await model.set_player_name(name)
    first_turn = random.randint(0,1)
    if first_turn:
        await view.player_take(message)
    else: await bot_turn(message)

async def player_turn(message: types.Message):
    game = await model.get_game()
    if game:
        take = 0
        if message.text == '/start':
            return
        else:
            take = int(message.text)
            print(take)
        if (take <= 28) and (take > 0):
            await model.set_total_count(take)
        else:
            await view.wrong_take(message)
            return
        name = await model.get_player_name()
        total_count = await model.get_total_count()
        if await model.get_total_count() > 0:
            await view.table_info(message, name, take, total_count, 'Бот')
            await bot_turn(message)
        else:
            await view.win(message, 'Игрок', take, total_count)
            await model.set_game()

async def bot_turn(message: types.Message):
    take = await model.bot_take()
    await model.set_total_count(take)
    name = await model.get_player_name()
    total_count = await model.get_total_count()
    if await model.get_total_count() > 0:
        await view.table_info(message, 'Бот', take, total_count, name)
    if await model.get_total_count() <= 0:
        await view.win(message, 'Бот', take, total_count)
        await model.set_game()

async def help(message):
    await view.help(message)


# app.add_handler(CommandHandler('start', start_game))
# app.add_handler(CommandHandler('help', help))
# app.add_handler(MessageHandler(filters.TEXT, player_turn))
# app.run_polling(drop_pending_updates=True)
