import discord
from discord.ext import commands

class Teams(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def test2(self, ctx):
        await ctx.send(self.bot.test)


async def setup(bot):
    await bot.add_cog(Teams(bot))