import json
import os

class ConfigGroup:
    def read(self, guild, key):
        if os.path.isfile(self._build_filename(guild)):
            with open(self._build_filename(guild), 'r', encoding='utf8') as readfile:
                data = json.load(readfile)
                if key in data:
                    return data.get(key)
                return None
                
        return None

    def write(self, guild, key, value):
        if os.path.isfile(self._build_filename(guild)):
            with open(self._build_filename(guild), 'r', encoding='utf8') as readfile:
                data = json.load(readfile)
        else:
            data = {}
        
        data[key] = value

        with open(self._build_filename(guild), 'w+', encoding='utf8') as outfile:
            json.dump(data, outfile, indent=True)

    def _build_filename(self, guild):
        path = "config/storage/{0}config.json"
        
        if guild == None:
            return path.format("")

        return path.format(str(guild) + "_")