from config.configgroup import ConfigGroup

class Birthday(ConfigGroup):
    def __init__(self):
        self.channel = {}
        self.engine = self.read(None, 'birthday_engine')
    
    def get_channel(self, guild):
        if guild in self.channel:
            return self.channel.get(guild)
        
        channel = self.read(guild, 'birthday_channel')
        
        self.channel[guild] = channel

        return channel

    def get_engine(self):
        return self.engine

    def set_channel(self, guild, channel):
        self.channel[guild] = channel

        self.write(guild, 'birthday_channel', channel)