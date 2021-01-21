import json
import os
from datetime import datetime

class CronJson():
    def read(self, key):
        if os.path.isfile(self._build_filename()):
            with open(self._build_filename(), 'r', encoding='utf8') as readfile:
                data = json.load(readfile)
                if key in data:
                    return data[key]
        return None

    def write(self, key, value):
        if os.path.isfile(self._build_filename()):
            with open(self._build_filename(), 'r', encoding='utf8') as readfile:
                data = json.load(readfile)
        else:
            data = {}

        data[key] = value
        data['updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(self._build_filename(), 'w+', encoding='utf8') as outfile:
            json.dump(data, outfile, indent=True)

    def _build_filename(self):
        return "bday/storage/cron.json"