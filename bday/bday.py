from datetime import datetime

class BDay:
    def __init__(self, guild_id, user_id, day, month, year):
        self.guild_id = guild_id
        self.user_id = user_id
        self.day = int(day)
        self.month = int(month)
        if year == None:
            self.year = None
        else:
            self.year = int(year)

        self.year_hidden = False

    def get_data(self):
        return {
            "guild" : self.guild_id,
            "user" : self.user_id,
            "year" : self.year,
            "month" : self.month,
            "day" : self.day,
            "hide_year" : self.year_hidden
        }
    
    def hide_year(self):
        self.year_hidden = True
    
    def show_year(self):
        self.year_hidden = False

    def is_year_hidden(self):
        return self.year_hidden

    def get_year(self):
        return self.year

    def get_birthday(self):
        return self._format(self.month) + '-' + self._format(self.day)

    def get_display_date(self):
        if self.year == None or self.year_hidden == True:
            return self._format(self.month) + '-' + self._format(self.day)
            
        return str(self.year) + '-' + self._format(self.month) + '-' + self._format(self.day)

    def get_age(self):
        if self.year == None or self.year_hidden == True:
            return None

        current_year = datetime.now().year
        current_month = datetime.now().month
        current_day = datetime.now().day

        age = current_year - self.year
        if current_month < self.month:
            age = age - 1
        elif current_month == self.month and current_day < self.day:
            age = age - 1

        return age

    def _format(self, number):
        if number < 10:
            return "0" + str(number)
        else:
            return str(number)

    def get_guild(self):
        return self.guild_id

    def get_user(self):
        return self.user_id