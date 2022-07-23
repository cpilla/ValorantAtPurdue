import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='>>', intents=discord.Intents.all())
        self.initial_extensions = [
            'cogs.utils',
            'cogs.sheets',
        ]
        self.sheet = None
    async def setup_hook(self):
        print(f"Logging in as: {self.user}")
        for ext in self.initial_extensions:
            await self.load_extension(ext)
        print(self.cogs)
        self.add_view(RegistrationMenu())
bot = MyBot()

class RegistrationMenu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout = None)

    @discord.ui.button(label="Register!", style=discord.ButtonStyle.green, custom_id="Register Button")
    async def reg_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = RankDropdownMenu()
        embed = discord.Embed(title = f'Select your current or previous act rank below.', color = discord.Colour.green())
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        await view.wait()
    
    @discord.ui.button(label="Un-Register!", style=discord.ButtonStyle.red, custom_id="Un-Register Button")
    async def unreg_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        removed = False
        for name in bot.sheet.col_values(1):
            if name == interaction.user.name:
                removed = True
                embed = discord.Embed(title = f'{bot.sheet.cell(bot.sheet.col_values(1).index(name) + 1, 1).value} ' + 
                                    f'is no longer registered as: {bot.sheet.cell(bot.sheet.col_values(1).index(name) + 1, 2).value} ' +
                                    f'for: {bot.sheet.cell(bot.sheet.col_values(1).index(name) + 1, 3).value}', 
                                    color = discord.Colour.red())
                await interaction.user.send(embed=embed)
                bot.sheet.delete_rows(bot.sheet.col_values(1).index(name) + 1)
                
        if not removed:
            embed = discord.Embed(title = f'{interaction.user.name} is not registered.', color = discord.Colour.yellow())
            await interaction.user.send(embed=embed)


        if(interaction.guild.get_role(748352636952117328) in interaction.user.roles):
            tryoutRole = interaction.guild.get_role(748352636952117328)
            await interaction.user.remove_roles(tryoutRole)
        await interaction.response.defer()

        

class RankDropdownMenu(discord.ui.View):
    def __init__(self):
        self.rank = None
        self.name = None
        super().__init__()
            
    selectOptions = [
        discord.SelectOption(label="Iron"),
        discord.SelectOption(label="Bronze"),
        discord.SelectOption(label="Silver"),
        discord.SelectOption(label="Gold"),
        discord.SelectOption(label="Platinum"),
        discord.SelectOption(label="Diamond"),
        discord.SelectOption(label="Ascendant 1"),
        discord.SelectOption(label="Ascendant 2"),
        discord.SelectOption(label="Ascendant 3"),
        discord.SelectOption(label="Immortal 1"),
        discord.SelectOption(label="Immortal 2"),
        discord.SelectOption(label="Immortal 3"),
        discord.SelectOption(label="Radiant"),
    ]

    @discord.ui.select(placeholder="Select your current or previous act rank!", options=selectOptions)
    async def test_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.name = interaction.user.name
        self.rank = select.values[0]
        view = RollDropdownMenu(self.name, self.rank)
        embed = discord.Embed(title = f'Select your main role here. \nOnly select two if you are EXTREMELY proficent in another.', color = discord.Colour.green())
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        await view.wait()
        self.stop()
        
class RollDropdownMenu(discord.ui.View):
    def __init__(self, name, rank):
        self.name = name
        self.rank = rank
        self.roles = []
        super().__init__()
            
    selectOptions = [
        discord.SelectOption(label="Controller"),
        discord.SelectOption(label="Initiator"),
        discord.SelectOption(label="Sentinel"),
        discord.SelectOption(label="Duelist"),
        discord.SelectOption(label="Flex"),
    ]

    @discord.ui.select(placeholder="Select 1-2 of your best roles!", options=selectOptions, min_values=1, max_values=2)
    async def test_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.stop()
        self.roles = select.values
        if "Ascendant" in self.rank or "Immortal" in self.rank or "Radiant" in self.rank:
            prospect = "Gold"
        elif "Diamond" in self.rank:
            prospect = "Black"
        else:
            prospect = "Gray/White"

        self.roles = '-'.join(str(x) for x in self.roles)

        inSheet = False

        for name in bot.sheet.col_values(1):
            if name == self.name:
                inSheet = True
                bot.sheet.update_cell(bot.sheet.col_values(1).index(name) + 1, 2, self.rank)
                bot.sheet.update_cell(bot.sheet.col_values(1).index(name) + 1, 3, self.roles)
                bot.sheet.update_cell(bot.sheet.col_values(1).index(name) + 1, 4, prospect)
        if not inSheet:
            bot.sheet.append_row([self.name, self.rank, self.roles, prospect])

        embed = discord.Embed(title = f'{self.name} has registered as: {self.rank} for: {self.roles}', color = discord.Colour.green())
        await interaction.user.send(embed=embed)
        tryoutRole = interaction.guild.get_role(748352636952117328)
        if tryoutRole not in interaction.user.roles:
            await interaction.user.add_roles(tryoutRole)
        await interaction.response.defer()

@bot.command()
@commands.is_owner()
async def spawn(ctx):
    if ctx.channel.id != 999905714149543936:
        await ctx.message.delete()
        return
    embed = discord.Embed(title = "Click here to register for tryouts!", color = 0xdaaa00)
    view = RegistrationMenu()
    if bot.regMessage == None:
        messages = [message async for message in ctx.message.channel.history(limit=1000)]
        await ctx.message.channel.delete_messages(messages)
        bot.regMessage = await ctx.send(embed=embed, view=view)
load_dotenv()
botKey = os.getenv("BOT_KEY")
bot.run(botKey)