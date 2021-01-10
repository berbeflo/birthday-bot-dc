from config.configgroup import ConfigGroup
import config.store.config as config

class Base(ConfigGroup):
    def __init__(self):
        self.token = config.token
        self.prefix = {}
    
    def get_token(self):
        return self.token

    def get_prefix(self, guild):
        if guild in self.prefix:
            return self.prefix.get(guild)
        
        prefix = self.read(guild, 'base_prefix')
        if prefix == None:
            prefix = self.read(None, 'base_prefix')
        
        self.prefix[guild] = prefix

        return prefix

    def set_prefix(self, guild, prefix):
        self.prefix[guild] = prefix

        self.write(guild, 'base_prefix', prefix)
