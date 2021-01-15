import json
import os
from bday.bday import BDay

class StorageJson():
    def find(self, guild_id, user_id):
        pass

    def read(self, guild_id, user_id):
        key = str(user_id)
        if os.path.isfile(self._build_filename(guild_id)):
            with open(self._build_filename(guild_id), 'r', encoding='utf8') as readfile:
                data = json.load(readfile)
                if key in data:
                    bd_data = data.get(key)
                    bday = BDay(bd_data['guild'], bd_data['user'], bd_data['day'], bd_data['month'], bd_data['year'])
                    if bd_data['hide_year'] == True:
                        bday.hide_year()
                    return bday
                return None
                
        return None

    def write(self, birthday):
        key = str(birthday.get_user())
        guild = birthday.get_guild()
        if os.path.isfile(self._build_filename(guild)):
            with open(self._build_filename(guild), 'r', encoding='utf8') as readfile:
                data = json.load(readfile)
        else:
            data = {}
        
        value = birthday.get_data()
        data[key] = value

        with open(self._build_filename(guild), 'w+', encoding='utf8') as outfile:
            json.dump(data, outfile, indent=True)

    def _build_filename(self, guild_id):
        return "bday/storage/{0}.json".format(guild_id)