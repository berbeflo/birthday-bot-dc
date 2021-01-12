from datetime import datetime

class BDay:
    def __init__(self, guild_id, day, month, year):
        self.guild_id = guild_id
        self.day = int(day)
        self.month = int(month)
        if year == None:
            self.year = None
        else:
            self.year = int(year)

        self.hide_year = False
    
    def hide_year(self):
        self.hide_year = True
    
    def show_year(self):
        self.hide_year = False

    def is_year_hidden(self):
        return self.hide_year

    def get_birthday(self):
        return str(self.month) + '-' + str(self.day)

    def get_display_date(self):
        if self.year == None or self.hide_year == True:
            return str(self.month) + '-' str(self.day)
            
        return str(self.year) + '-' + str(self.month) + '-' str(self.day)

    def get_age(self):
        if self.year == None or self.hide_year == True:
            return None

        current_year = datetime.now().year
        current_month = datetime.now().month
        current_day = datetime.now().day

        age = current_year - self.year
        if current_month < self.month:
            age = age - 1
        elif current_month == self.month and current_day < self.day
            age = age - 1

        return age