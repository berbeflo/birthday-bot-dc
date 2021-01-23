from discord.ext import tasks
from datetime import datetime
from config.config import config
from bday.engine.engine import engine

class BdCron():
    def __init__(self, bot):
        self.bot = bot
        self.engine = engine
        self.congratulate.start()

    @tasks.loop(seconds=60)
    async def congratulate(self):
        if self.congratulate.current_loop < 2:
            return
        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        last_date = self.engine.cron().read('last_date')

        if date == last_date:
            return
        
        await self._process_birthdays(now)

        self.engine.cron().write('last_date', date)

    async def _process_birthdays(self, now):
        for guild in self.bot.guilds:
            guild_channel = config.birthday.get_channel(guild.id)
            if guild_channel == None:
                continue
            guild_channel = guild.get_channel(guild_channel)
            if guild_channel == None:
                continue

            bd_role = await self.__get_bdrole(guild)

            month = int(now.strftime("%m"))
            day = int(now.strftime("%d"))
            bday_users = self.engine.storage().find(guild.id, month, day)

            for user_id in bday_users:
                bday = self.engine.storage().read(guild.id, user_id)
                user = await guild.fetch_member(user_id)

                if user == None:
                    continue

                if bd_role != None:
                    await user.add_roles(bd_role, reason="It's their birthday <3")
                
                age = bday.get_age()
                if age == None:
                    await guild_channel.send("It's the birthday of {0}.".format(user.mention))
                else:
                    await guild_channel.send("It's the birthday of {0}. They got {1} years old.".format(user.mention, age))
                age = bday.get_age(True)
                if age != None:
                    await self.__set_agerole(guild, user, age)

    async def __get_bdrole(self, guild):
        bot = await self.__get_bot_member(guild)
        role = config.birthday.get_role(guild.id)
        highest_bot_role = bot.roles[-1]

        if role == None:
            return None

        role_object = guild.get_role(role)
        if role_object == None:
            return None

        if highest_bot_role <= role_object:
            return None

        await self.__clear_role(role_object)

        return role_object

    async def __get_bot_member(self, guild):
        bot_user_id = self.bot.user.id
        member = await guild.fetch_member(bot_user_id)
        
        return member

    async def __clear_role(self, role):
        members = role.members
        for member in members:
            await member.remove_roles(role, reason="Oh, their birthday was yesterday :(")

    async def __set_agerole(self, guild, user, member_age):
        role_settings = config.birthday.get_ageroles(guild.id)
        if role_settings == None or len(role_settings) == 0:
            return
        
        ages = list(map(lambda v : int(v), sorted(role_settings, key=lambda k : int(k))))

        if not member_age in ages:
            return

        for age in ages:
            role = role_settings[str(age)]
            role_object = guild.get_role(role)

            if role_object == None:
                continue

            if role_object in user.roles:
                await user.remove_roles(role_object, reason='Update on birthday')
                break

        use_age = None
        for age in ages:
            if member_age >= age:
                use_age = str(age)
            else:
                break

        if use_age != None:
            role = role_settings[use_age]
            role_object = guild.get_role(role)
            await user.add_roles(role_object, reason = 'Update on birthday')

def setup(bot):
    BdCron(bot)