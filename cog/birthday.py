import discord
from discord.ext import commands
from config.config import config
from re import match

class Birthday(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(Birthday(bot))