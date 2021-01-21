from config.config import config
from bday.engine.cron_json import CronJson
from bday.engine.cron_sqlite import CronSqLite
from bday.engine.storage_json import StorageJson
from bday.engine.storage_sqlite import StorageSqLite

class Engine():
    def __init__(self):
        if config.birthday.get_engine() == "json":
            self.__load_json_engines()
        elif config.birthday.get_engine() == "sqlite":
            self.__load_sqlite_engines()
        else:
            raise Exception('no such engine {0}'.format(config.birthday.get_engine()))

    def __load_json_engines(self):
        self.storage_engine = StorageJson()
        self.cron_engine = CronJson()

    def __load_sqlite_engines(self):
        self.storage_engine = StorageSqLite()
        self.cron_engine = CronSqLite()

    def storage(self):
        return self.storage_engine

    def cron(self):
        return self.cron_engine

engine = Engine()