import logging
import traceback
from datetime import datetime

import discord
from discord.ext import commands

from config import bot_token, owner_id


class Bot(discord.Client):
    def __init__(self, **kwargs):
        super().__init__(
            command_prefix=self.command_prefix,
            owner_id=owner_id,
            self_bot=True,
        )
        handler = logging.StreamHandler()
        dt_fmt = "%H:%M:%S %d-%m-%Y"
        formatter = logging.Formatter(
            "{asctime} {levelname:<5} {name}: {message}", dt_fmt, style="{"
        )
        handler.setFormatter(formatter)
        file_handler = logging.FileHandler(
            filename="log.txt", mode="a", encoding="UTF-8"
        )
        file_handler.setFormatter(formatter)
        logger = logging.getLogger("discord")
        logger.addHandler(handler)
        logger.addHandler(file_handler)
        logging.getLogger("discord").setLevel(logging.INFO)
        logging.getLogger("discord.http").setLevel(logging.WARNING)
        logging.getLogger("discord.gateway").setLevel(logging.WARNING)

        self.log = logger
        ###
        self.start_time = None

    @staticmethod
    def command_prefix(self, message: discord.Message):
        prefixes = [">"]
        return commands.when_mentioned_or(*prefixes)(self, message)

    async def on_connect(self):
        self.log.info(
            f"Logged in as: {self.user.name} - {self.user.id}\nVersion: {discord.__version__}\n"
        )
        await self.change_presence(status=discord.Status.dnd)
        self.log.info("Successfully loaded, the initialization of the modules...")

        self.start_time = datetime.utcnow()

    def listen_to_exceptions(self, event):
        self.loop.create_task(self.listen_to_exceptions_async(event))

    async def listen_to_exceptions_async(self, event):
        error_str = traceback.format_exception(
            type(event.exception), event.exception, event.exception.__traceback__
        )
        error_str = "".join(error_str)
        self.log.error(error_str)

    async def on_error(self, event, *args, **kwargs):
        error = traceback.format_exc()
        error_msg = (
            f"\nevent:\n{event}\nargs:\n{args}\nkwargs:\n{kwargs}\nerror:\n{error}"
        )
        self.log.error(error_msg)

    async def on_message(self, message: discord.Message):
        self.log.info(
            f"\nUser: {message.author}\nUrl: {message.jump_url}\nContent: {message.content}\n"
        )


bot = Bot()
bot.run(bot_token)
