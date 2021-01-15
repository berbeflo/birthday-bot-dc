import discord
from discord.ext import commands
from config.config import config
from re import search
from datetime import datetime
from bday.engine.storage_json import StorageJson
from bday.bday import BDay
import typing

class Birthday(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.storage = None
        if config.birthday.get_engine() == "json":
            self.storage = StorageJson()

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
        
        birthday = BDay(ctx.message.guild.id, ctx.message.author.id, match_dict["day"], match_dict["month"], match_dict["year"])
        self.storage.write(birthday)

        await ctx.send('Your birthday was stored')
        await ctx.message.delete()

    @commands.command()
    async def when(self, ctx, user: typing.Optional[discord.User] = None):
        if user == None:
            user = ctx.message.author
        user_id = user.id

        birthday = self.storage.read(ctx.message.guild.id, user_id)
        if birthday == None:
            await ctx.send('The user did not tell me his birthday.')
            return

        if birthday.is_year_hidden() or birthday.get_year() == None:
            await ctx.send('{0} has birthday at {1}'.format(user.name, birthday.get_birthday()))
        else:
            await ctx.send('{0} has birthday at {1} and is currently {2} years old'.format(user.name, birthday.get_birthday(), birthday.get_age()))

    @commands.command()
    async def who(self, ctx, date):
        match = search(r"^(?P<month>\d{2})-(?P<day>\d{2})$", date)
        if match == None:
            match = search(r"^(?P<day>\d{2})\.(?P<month>\d{2})\.$", date)
        if match == None:
            await ctx.send('The date does not match the awaited syntax')
            return
        match_dict = match.groupdict()

        day = int(match_dict["day"])
        month = int(match_dict["month"])

        users = self.storage.find(ctx.message.guild.id, month, day)
        members = []
        print(users)
        for user in users:
            try:
                member = await ctx.message.guild.fetch_member(user)
                members.append(member)
            except:
                pass

        if len(members) == 0:
            await ctx.send('There are no users that have birthday on {0}'.format(date))
            return

        member_string = ""
        first = True
        for member in members:
            if first == False:
                member_string = member_string + ", "
            first = False
            member_string = member_string + member.display_name + " (" + member.name + "#" + member.discriminator + ")"

        await ctx.send('The following users have birthday on {0}: {1}'.format(date, member_string))
        
    @commands.command()
    async def hide_age(self, ctx):
        birthday = self.storage.read(ctx.message.guild.id, ctx.message.author.id)
        if birthday == None:
            await ctx.send('You did not tell me your birthday yet.')
            return

        birthday.hide_year()

        self.storage.write(birthday)

        await ctx.send('Your age will now be hidden.')

    @commands.command()
    async def show_age(self, ctx):
        birthday = self.storage.read(ctx.message.guild.id, ctx.message.author.id)
        if birthday == None:
            await ctx.send('You did not tell me your birthday yet.')
            return

        birthday.show_year()

        self.storage.write(birthday)

        if birthday.get_year() == None:
            await ctx.send('This had no effect, as you did not provide your year of birth.')
        else:
            await ctx.send('Your age will now be shown.')

def setup(bot):
    bot.add_cog(Birthday(bot))