from config.configgroup import ConfigGroup

class Birthday(ConfigGroup):
    def __init__(self):
        self.channel = {}
        self.role = {}
        self.ageroles = {}
        self.engine = self.read(None, 'birthday_engine')

    def get_role(self, guild):
        if guild in self.role:
            return self.role.get(guild)

        role = self.read(guild, 'birthday_role')

        self.role[guild] = role

        return role

    def set_role(self, guild, role):
        self.role[guild] = role

        self.write(guild, 'birthday_role', role)

    def get_ageroles(self, guild):
        if guild in self.ageroles:
            return self.ageroles.get(guild)

        ageroles = self.read(guild, 'birthday_ageroles')

        self.ageroles[guild] = ageroles

        return ageroles

    def set_ageroles(self, guild, ageroles):
        self.ageroles[guild] = ageroles

        self.write(guild, 'birthday_ageroles', ageroles)
    
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