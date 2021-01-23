import discord
from discord.ext import commands
from config.config import config
from re import search
from datetime import datetime
from bday.engine.engine import engine
from bday.bday import BDay
import typing

class Birthday(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.engine = engine

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
        self.engine.storage().write(birthday)

        await self.__refresh_roles(ctx.message.guild, ctx.message.author, birthday)

        await ctx.send('Your birthday was stored')
        await ctx.message.delete()

    @commands.command()
    async def when(self, ctx, user: typing.Optional[discord.User] = None):
        if user == None:
            user = ctx.message.author
        user_id = user.id

        birthday = self.engine.storage().read(ctx.message.guild.id, user_id)
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

        users = self.engine.storage().find(ctx.message.guild.id, month, day)
        members = []
        
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
        birthday = self.engine.storage().read(ctx.message.guild.id, ctx.message.author.id)
        if birthday == None:
            await ctx.send('You did not tell me your birthday yet.')
            return

        birthday.hide_year()

        self.engine.storage().write(birthday)

        await ctx.send('Your age will now be hidden.')

    @commands.command()
    async def show_age(self, ctx):
        birthday = self.engine.storage().read(ctx.message.guild.id, ctx.message.author.id)
        if birthday == None:
            await ctx.send('You did not tell me your birthday yet.')
            return

        birthday.show_year()

        self.engine.storage().write(birthday)

        if birthday.get_year() == None:
            await ctx.send('This had no effect, as you did not provide your year of birth.')
        else:
            await ctx.send('Your age will now be shown.')

    @commands.has_permissions(administrator=True)
    @commands.group(pass_context=True, invoke_without_command=False)
    async def bdayrole(self, ctx):
        pass

    @bdayrole.command(name='set')
    async def bdayrole_set(self, ctx, role: typing.Optional[discord.Role]):
        roles = ctx.me.roles
        highest_role = roles[-1]

        if role == None:
            config.birthday.set_role(ctx.message.guild.id, None)
            await ctx.send('Removed the birthday role')
            return

        if highest_role <= role:
            await ctx.send('The bot cannot give this role to any member')
            return

        config.birthday.set_role(ctx.message.guild.id, role.id)
        await ctx.send('Set the role {0} as birthday role'.format(role.mention))

    @bdayrole.command(name='get')
    async def bdayrole_get(self, ctx):
        role = config.birthday.get_role(ctx.message.guild.id)
        role_object = ctx.message.guild.get_role(role)
        roles = ctx.me.roles
        highest_role = roles[-1]

        if highest_role <= role_object:
            role_object = None

        if role_object == None:
            await ctx.send('This server has currently no (valid) birthday role')
            return

        await ctx.send('The current birthday role for this server is {0}'.format(role_object.mention))

    @commands.has_permissions(administrator=True)
    @commands.group(pass_context=True, invoke_without_command=False)
    async def agerole(self, ctx):
        pass
    
    @agerole.command(name='add')
    async def agerole_add(self, ctx, age : int, role : discord.Role):
        highest_bot_role = ctx.me.roles[-1]

        if highest_bot_role <= role:
            await ctx.send('The bot cannot assign this role')
            return

        age = str(age)
        role_settings = config.birthday.get_ageroles(ctx.message.guild.id)

        if role_settings == None:
            role_settings = {}

        role_settings[age] = role.id

        config.birthday.set_ageroles(ctx.message.guild.id, role_settings)

        await ctx.send('Added role {0} for age {1}+'.format(role.mention, age))

    @agerole.command(name='remove')
    async def agerole_remove(self, ctx, age : int):
        age = str(age)

        role_settings = config.birthday.get_ageroles(ctx.message.guild.id)

        if role_settings == None or not age in role_settings:
            await ctx.send('There is no role for this age')
            return

        del role_settings[age]

        config.birthday.set_ageroles(ctx.message.guild.id, role_settings)

        await ctx.send('Removed the role for age {0}+'.format(age))

    @agerole.command(name='list')
    async def agerole_list(self, ctx):
        role_settings = config.birthday.get_ageroles(ctx.message.guild.id)

        if role_settings == None or len(role_settings) == 0:
            await ctx.send('There are currently no age roles configured')
        
        for key in sorted(role_settings, key=lambda k: int(k)):
            role_object = ctx.message.guild.get_role(role_settings[key])
            if role_object != None:
                await ctx.send('The role {0} is assigned for age {1}+'.format(role_object.mention, key))
            else:
                await ctx.send('The role for age {0}+ does not exist anymore'.format(key))

    @agerole.command(name='refresh')
    async def agerole_refresh(self, ctx):
        guild = ctx.message.guild
        role_ages = config.birthday.get_ageroles(guild.id)
        ages = list(map(lambda v : int(v), sorted(role_ages, key=lambda k : int(k))))
        role_objects = {}

        for age in ages:
            age = str(int(age))
            role = role_ages[age]
            role_object = guild.get_role(role)

            role_objects[age] = role_object

            if role_object == None:
                continue

            for member in role_object.members:
                await member.remove_roles(role_object, reason='Refreshing the age roles')

        bd_members = self.engine.storage().all(guild.id)
        
        for user_id in bd_members:
            birthday = self.engine.storage().read(guild.id, user_id)

            member_age = birthday.get_age(True)
            if member_age == None:
                continue

            use_age = None
            for age in ages:
                if member_age >= age:
                    use_age = str(age)
                else:
                    break

            if use_age == None:
                continue

            member = await guild.fetch_member(user_id)
            if member == None:
                continue

            new_role = role_objects[use_age]
            if new_role == None:
                continue

            await member.add_roles(new_role, reason='Refreshing the age roles')

        await ctx.send('Refreshed the age roles')

    async def __refresh_roles(self, guild, user, member_bday):
        member_age = member_bday.get_age(True)
        role_settings = config.birthday.get_ageroles(guild.id)
        bd_role = config.birthday.get_role(guild.id)
        bd_role_object = guild.get_role(bd_role)
        ages = list(map(lambda v : int(v), sorted(role_settings, key=lambda k : int(k))))

        if bd_role_object != None:
            await user.remove_roles(bd_role_object, reason='The user updated their birthday')
            if member_bday.has_birthday():
                await user.add_roles(bd_role_object, reason='The user updated their birthday')

        use_age = None
        for age in ages:
            role = role_settings[str(age)]
            role_object = guild.get_role(role)
            
            if member_age != None and member_age >= age:
                use_age = str(age)
            
            await user.remove_roles(role_object, reason='The user updated their birthday')

        if use_age == None:
            return

        role_object = guild.get_role(role_settings[use_age])
        if role_object == None:
            return
        
        await user.add_roles(role_object, reason='The user updated their birthday')

        

def setup(bot):
    bot.add_cog(Birthday(bot))