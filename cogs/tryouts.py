import discord
from discord.ext import commands
import cogs.sheets as sheets


class Tryouts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.regMessage = None
        bot.tryoutsSheet = sheets.get_sheet(bot, "Tryouts")
    
    @commands.Cog.listener()
    async def on_ready(self):
        #Basically run spawn command
        return
    
    @commands.command()
    async def spawn(self, ctx):
        embed = discord.Embed(title = "Click here to register for tryouts!", color = 0xdaaa00)
        view = RegistrationMenu(self.bot)
        if self.bot.regMessage == None:
            messages = [message async for message in ctx.message.channel.history(limit=100)]
            await ctx.message.channel.delete_messages(messages)
            self.bot.regMessage = await ctx.send(embed=embed, view=view)
    
    @commands.command()
    async def reorg(self, ctx):
        reorg_sheet(self.bot.tryoutsSheet, sheets.get_sheet(self.bot, "test"))


class RegistrationMenu(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout = None)
        self.bot = bot

    @discord.ui.button(label="Register!", style=discord.ButtonStyle.green, custom_id="Register Button")
    async def reg_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = RankDropdownMenu(self.bot)
        embed = discord.Embed(title = f'Select your current or previous act rank below.', color = discord.Colour.green())
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        await view.wait()
    
    @discord.ui.button(label="Un-Register!", style=discord.ButtonStyle.red, custom_id="Un-Register Button")
    async def unreg_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        removed = False
        for name in self.bot.tryoutsSheet.col_values(1):
            if name == interaction.user.name:
                removed = True
                embed = discord.Embed(title = f'{self.bot.tryoutsSheet.cell(self.bot.tryoutsSheet.col_values(1).index(name) + 1, 1).value} ' + 
                                    f'is no longer registered as: {self.bot.tryoutsSheet.cell(self.bot.tryoutsSheet.col_values(1).index(name) + 1, 2).value} ' +
                                    f'for: {self.bot.tryoutsSheet.cell(self.bot.tryoutsSheet.col_values(1).index(name) + 1, 3).value}', 
                                    color = discord.Colour.red())
                await interaction.user.send(embed=embed)
                self.bot.tryoutsSheet.delete_rows(self.bot.tryoutsSheet.col_values(1).index(name) + 1)
                
        if not removed:
            embed = discord.Embed(title = f'{interaction.user.name} is not registered.', color = discord.Colour.yellow())
            await interaction.user.send(embed=embed)


        if(interaction.guild.get_role(748352636952117328) in interaction.user.roles):
            tryoutRole = interaction.guild.get_role(748352636952117328)
            await interaction.user.remove_roles(tryoutRole)
        await interaction.response.defer()

class RankDropdownMenu(discord.ui.View):
    def __init__(self, bot):
        self.rank = None
        self.name = None
        super().__init__()
        self.bot = bot
            
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
        view = RollDropdownMenu(self.name, self.rank, self.bot)
        embed = discord.Embed(title = f'Select your main role here. \nOnly select two if you are EXTREMELY proficent in another.', color = discord.Colour.green())
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        await view.wait()
        self.stop()
        
class RollDropdownMenu(discord.ui.View):
    def __init__(self, name, rank, bot):
        self.name = name
        self.rank = rank
        self.roles = []
        self.bot = bot
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

        for name in self.bot.tryoutsSheet.col_values(1):
            if name == self.name:
                inSheet = True
                self.bot.tryoutsSheet.update_cell(self.bot.tryoutsSheet.col_values(1).index(name) + 1, 2, self.rank)
                self.bot.tryoutsSheet.update_cell(self.bot.tryoutsSheet.col_values(1).index(name) + 1, 3, self.roles)
                self.bot.tryoutsSheet.update_cell(self.bot.tryoutsSheet.col_values(1).index(name) + 1, 4, prospect)
        if not inSheet:
            self.bot.tryoutsSheet.append_row([self.name, self.rank, self.roles, prospect])

        embed = discord.Embed(title = f'{self.name} has registered as: {self.rank} for: {self.roles}', color = discord.Colour.green())
        await interaction.user.send(embed=embed)
        tryoutRole = interaction.guild.get_role(748352636952117328)
        if tryoutRole not in interaction.user.roles:
            await interaction.user.add_roles(tryoutRole)
        await interaction.response.defer()

def reorg_sheet(sheet):
    gold = [[]]
    black = [[]]
    gw = [[]]
    index = 0

    for team in sheet.col_values(4):
        index = index + 1
        
        if team == "Gold":
            if gold[0] == []:
                gold[0] = sheet.row_values(index)
            else:
                gold.append(sheet.row_values(index))
        elif team == "Black":
            if black[0] == []:
                black[0] = sheet.row_values(index)
            else:
                black.append(sheet.row_values(index))
        elif team == "Gray/White":
            if gw[0] == []:
                gw[0] = sheet.row_values(index)
            else:
                gw.append(sheet.row_values(index))
    for player in black:
        gold.append(player)
    for player in gw:
        gold.append(player)

    sheet.batch_update([{'range' : "A2:D100", 'values': gold}])
    print("did")



async def setup(bot):
    await bot.add_cog(Tryouts(bot))
    bot.add_view(RegistrationMenu(bot))