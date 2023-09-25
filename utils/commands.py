from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_default_commands(bot: Bot):
    commands = ([
        BotCommand(command="start",
                   description="Жми в любой непонятной ситуации"),
        BotCommand(command="info",
                   description="Все, что нужно знать о сервисе"),
        BotCommand(command="referrals",
                   description="Реферальный кабинет")

    ])

    await bot.set_my_commands(commands,
                              BotCommandScopeDefault())
