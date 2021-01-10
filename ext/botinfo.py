class BotInfo:
    owner = None

    def __init__(self, bot):
        self.bot = bot

    async def setup(self):
        self.info = await self.bot.application_info()
        self.owner = self.info.owner

    def is_owner(self, user_id):
        return self.owner.id == user_id

info = None
def setup(bot):
    global info
    info = BotInfo(bot)