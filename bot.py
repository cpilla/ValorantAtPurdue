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
            'cogs.teams',
        ]
    async def setup_hook(self):
        print(f"Logging in as: {self.user}")
        for ext in self.initial_extensions:
            await self.load_extension(ext)
        print(self.cogs)

bot = MyBot()

@bot.command()
async def test(ctx):
    await ctx.send(bot.test)

load_dotenv()
botKey = os.getenv("BOT_KEY")
bot.run(botKey)