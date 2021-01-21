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

            month = int(now.strftime("%m"))
            day = int(now.strftime("%d"))
            bday_users = self.engine.storage().find(guild.id, month, day)

            for user_id in bday_users:
                bday = self.engine.storage().read(guild.id, user_id)
                user = await guild.fetch_member(user_id)

                if user == None:
                    continue
                
                age = bday.get_age()
                if age == None:
                    await guild_channel.send("It's the birthday of {0}.".format(user.mention))
                else:
                    await guild_channel.send("It's the birthday of {0}. They got {1} years old.".format(user.mention, age))

def setup(bot):
    BdCron(bot)