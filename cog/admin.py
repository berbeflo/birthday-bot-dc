import discord
from discord.ext import commands
from config.config import config
from re import match

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def reload(self, ctx, extension):
        if extension in self.bot.extensions:
            self.bot.reload_extension(extension)
            await ctx.send('done reloading extension ' + extension)
        else:
            await ctx.send('extension ' + extension + ' not found')

def setup(bot):
    bot.add_cog(Admin(bot))