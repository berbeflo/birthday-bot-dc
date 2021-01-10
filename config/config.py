from config.group.base import Base
from config.group.birthday import Birthday

class Config:
    base = None
    birthday = None

    def __init__(self):
        self.base = Base()
        self.birthday = Birthday()

config = Config()