from config.group.base import Base

class Config:
    base = None

    def __init__(self):
        self.base = Base()

config = Config()