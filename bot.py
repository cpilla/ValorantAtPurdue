import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import discord.ui

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='>>', intents=discord.Intents.all())
        self.initial_extensions = [
            'cogs.utils',
            'cogs.sheets',
            'cogs.tryouts',
        ]
        self.sheet = None
        self.regMessage = None
    async def setup_hook(self):
        print(f"Logging in as: {self.user}")
        for ext in self.initial_extensions:
            await self.load_extension(ext)
        print(self.cogs)

bot = MyBot()

load_dotenv()
botKey = os.getenv("BOT_KEY")
bot.run(botKey)