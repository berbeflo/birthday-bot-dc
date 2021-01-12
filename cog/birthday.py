import discord
from discord.ext import commands
from config.config import config
from re import search
from datetime import datetime

class Birthday(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def set(self, ctx, date):
        match = search(r"^((?P<year>\d{4})-)?(?P<month>\d{2})-(?P<day>\d{2})$", date)
        if match == None:
            match = search(r"^(?P<day>\d{2})\.(?P<month>\d{2})\.(?P<year>\d{4})?$", date)
        if match == None:
            await ctx.send('The date does not match the awaited syntax')
            return

        current_year = datetime.now().year
        match_dict = match.groupdict()
        given_year = match_dict['year']
        test_year = "2004"

        if given_year != None:
            test_year = given_year
            year_diff = current_year - int(given_year)
            if not 10 < year_diff < 100:
                await ctx.send('The given year is not valid')
                return
        
        test_string = test_year + "-" + match_dict['month'] + "-" + match_dict['day']
        try:
            dt_obj = datetime.strptime(test_string, '%Y-%m-%d')
        except:
            await ctx.send('The given date is not valid')
            return
        
        print(match.groupdict())

def setup(bot):
    bot.add_cog(Birthday(bot))