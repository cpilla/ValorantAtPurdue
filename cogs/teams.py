import discord
from discord.ext import commands
import cogs.sheets as sheets

class Teams(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.teamDatabaseSheet = sheets.get_sheet(bot, "Team Database")
        bot.teams = {
            "Gold": {},
            "Black": {},
            "Gray": {},
            "White": {},
        }
        populateTeams(bot.teams)
        
    
    @commands.Cog.listener()
    async def on_ready(self):
        #Bump embed
        return


    @commands.command()
    async def print_team_info(self, ctx, nf):
        cells = sheets.get_data_from_nf(self.bot.teamDatabaseSheet, nf)
        await ctx.send(cells)

class ManagementMenu(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout = None)
        self.bot = bot

    @discord.ui.button(label="Register!", style=discord.ButtonStyle.green, custom_id="Register Button")
    async def reg_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()

    @discord.ui.button(label="Register!", style=discord.ButtonStyle.green, custom_id="Register Button")
    async def reg_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()

    @discord.ui.button(label="Register!", style=discord.ButtonStyle.green, custom_id="Register Button")
    async def reg_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
    




def populateTeams(teams):
    return

    
async def setup(bot):
    await bot.add_cog(Teams(bot))