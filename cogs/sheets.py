from discord.ext import commands
from googleapiclient.discovery import build
import gspread
from oauth2client.service_account import ServiceAccountCredentials

class Sheets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        print("Initializing Google Authentication...")
        scope = ["https://spreadsheets.google.com/feeds",
                'https://www.googleapis.com/auth/spreadsheets',
                "https://www.googleapis.com/auth/drive.file",
                "https://www.googleapis.com/auth/drive"]  
        creds = ServiceAccountCredentials.from_json_keyfile_name("sheet-user.json", scope)
        client = gspread.authorize(creds)
        bot.client = client
        sheet = client.open("Tryouts2022").sheet1  # Open the spreadhseet
        bot.sheet = sheet

async def setup(bot):
    await bot.add_cog(Sheets(bot))