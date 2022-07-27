import discord
from discord.ext import commands
import cogs.sheets as sheets
from table2ascii import table2ascii as t2a, PresetStyle

class Teams(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.teamDatabaseSheet = sheets.get_sheet(bot, "Team Database")
        
    #@commands.Cog.listener()
    #async def on_ready(self):
        #channel = self.bot.get_channel(1001406133946294413)
        #await channel.purge(limit=100)
        #embed = discord.Embed(title="Team Management Menu", description="Select a team below to view management options and overview.", colour=discord.Color.green())
        #view = ManagementMenu(self.bot)
        #await channel.send(embed=embed, view=view)

    @commands.command()
    async def print_team_info(self, ctx, nf):
        cells = sheets.get_data_from_nf(self.bot.teamDatabaseSheet, nf)
        await ctx.send(cells)

class ManagementMenu(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout = None)
        self.bot = bot

    @discord.ui.button(label="Gold", style=discord.ButtonStyle.blurple, custom_id="gold_button")
    async def gold_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = format_team_table_from_data(self.bot.teamDatabaseSheet, "Gold")
        self.bot.teamDatabaseSheet.range()
        await interaction.response.send_message(embed, ephemeral=True)

    @discord.ui.button(label="Black", style=discord.ButtonStyle.blurple, custom_id="black_button")
    async def black_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = format_team_table_from_data(self.bot.teamDatabaseSheet, "Black")
        await interaction.response.send_message(embed, ephemeral=True)

    @discord.ui.button(label="Gray", style=discord.ButtonStyle.blurple, custom_id="gray_button")
    async def gray_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = format_team_table_from_data(self.bot.teamDatabaseSheet, "Gray")
        await interaction.response.send_message(embed, ephemeral=True)
    
    @discord.ui.button(label="White", style=discord.ButtonStyle.blurple, custom_id="white_button")
    async def white_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = format_team_table_from_data(self.bot.teamDatabaseSheet, "White")
        await interaction.response.send_message(embed, ephemeral=True)

    @discord.ui.button(label="Overview", style=discord.ButtonStyle.blurple, custom_id="overview_button", row=2)
    async def overview_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
    
    @discord.ui.button(label="Bump", style=discord.ButtonStyle.blurple, custom_id="clean_button", row=2)
    async def clean_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        channel = self.bot.get_channel(1001406133946294413)
        await channel.purge(limit=100)

        embed = discord.Embed(title="Team Management Menu", description="Select a team below to view management options and overview.", colour=discord.Color.green())
        view = ManagementMenu(self.bot)
        await channel.send(embed=embed, view=view)

        await interaction.response.defer()

def add_player(worksheet, player, team):
    namedRange = f'Team{team}'
    return


def format_team_table_from_data(worksheet, team):
    namedRange = f'Team{team}'
    data = sheets.get_data_from_nf(worksheet, namedRange)
    numPlayers = 0
    for row in data[1:]:
        if not row[0] == '':
            numPlayers = numPlayers + 1

    table = t2a(
        header=data[0],
        body=data[1:numPlayers + 1],
        style=PresetStyle.thin_compact)
    return f"```\n{table}\n```"

async def setup(bot):
    await bot.add_cog(Teams(bot))
    bot.add_view(ManagementMenu(bot))