import os
from bday.bday import BDay
import sqlite3

class StorageSqLite:
    version = '1.0'

    def __init__(self):
        file = 'bday/storage/birthdays.db'
        new = True
        if os.path.isfile(file):
            new = False

        con = sqlite3.connect(file)
        con.row_factory = sqlite3.Row

        self.connection = con

        if new:
            cursor = self.connection.cursor()
            cursor.execute('''
                create table version (
                    version text not null,
                    installed text not null
                );
            ''')
            cursor.execute('''
                insert into version
                    (version, installed)
                    values
                    (?, datetime('now'));
            ''', (self.version,))
            cursor.execute('''
                create table birthdays (
                    guild char(20) not null,
                    user char(20) not null,
                    day int not null,
                    month int not null,
                    year int,
                    hide_year int not null,
                    primary key (guild, user)
                );
            ''')

            self.connection.commit()
            
    def write(self, birthday):
        data = birthday.get_data()
        cursor = self.connection.cursor()
        cursor.execute('''
            delete from birthdays
                where guild = ? and user = ?;
        ''', (data['guild'], data['user']))
        cursor.execute('''
            insert into birthdays
                (guild, user, day, month, year, hide_year)
                values
                (?, ?, ?, ?, ?, ?);
        ''', (data['guild'], data['user'], data['day'], data['month'], data['year'], data['hide_year']))

        self.connection.commit()

    def read(self, guild_id, user_id):
        cursor = self.connection.cursor()
        cursor.execute('''
            select * from birthdays
                where guild = ? and user = ?;
        ''', (guild_id, user_id))
        result = cursor.fetchone()
        if result == None:
            return None
        
        bday = BDay(result["guild"], result["user"], result["day"], result["month"], result["year"])
        if result["hide_year"] == 1:
            bday.hide_year()

        return bday

    def find(self, guild_id, month, day):
        users = []
        cursor = self.connection.cursor()
        cursor.execute('''
            select user from birthdays
                where guild = ? and month = ? and day = ?;
        ''', (guild_id, month, day))

        result = cursor.fetchall()
        for row in result:
            users.append(row["user"])

        return users

    def all(self, guild_id):
        users = []
        cursor = self.connection.cursor()
        cursor.execute('''
            select user from birthdays
                where guild = ?
        ''', (guild_id, ))

        result = cursor.fetchall()
        for row in result:
            users.append(row["user"])

        return users