from discord.ext import tasks
from datetime import datetime
from config.config import config
from bday.engine.cron_json import CronJson
from bday.engine.storage_json import StorageJson
from bday.engine.storage_sqlite import StorageSqLite

class BdCron():
    def __init__(self, bot):
        self.bot = bot
        self.cron_engine = self._get_cron_engine()
        self.storage_engine = self._get_storage_engine()
        self.congratulate.start()

    @tasks.loop(seconds=5)
    async def congratulate(self):
        if self.congratulate.current_loop < 2:
            return
        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        last_date = self.cron_engine.read('last_date')

        if date == last_date:
            pass
        
        await self._process_birthdays(now)

        self.cron_engine.write('last_date', date)

    def _get_cron_engine(self):
        if config.birthday.get_engine() == "json":
            return CronJson()

        raise Exception('no engine loaded')

    def _get_storage_engine(self):
        if config.birthday.get_engine() == "json":
            return StorageJson()
        if config.birthday.get_engine() == "sqlite":
            return StorageSqLite()

        raise Exception('no engine loaded')

    async def _process_birthdays(self, now):
        for guild in self.bot.guilds:
            guild_channel = config.birthday.get_channel(guild.id)
            if guild_channel == None:
                continue
            guild_channel = guild.get_channel(guild_channel)
            if guild_channel == None:
                continue
            print(guild_channel.name)

            month = int(now.strftime("%m"))
            day = int(now.strftime("%d"))
            bday_users = self.storage_engine.find(guild.id, month, day)

            for user_id in bday_users:
                bday = self.storage_engine.read(guild.id, user_id)
                print(user_id)
                user = await guild.fetch_member(user_id)

                print(user)
                if user == None:
                    continue
                
                age = bday.get_age()
                print(age)
                if age == None:
                    await guild_channel.send("It's the birthday of {0}.".format(user.mention))
                else:
                    await guild_channel.send("It's the birthday of {0}. They got {1} years old.".format(user.mention, age))

def setup(bot):
    BdCron(bot)