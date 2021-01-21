import sqlite3
import os

class CronSqLite():
    version = '1.0'
    
    def __init__(self):
        file = 'bday/storage/cron.db'
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
                create table cron (
                    id int not null,
                    last_date text,
                    updated_at text not null,
                    primary key (id)
                );
            ''')
            cursor.execute('''
                insert into cron
                    (id, last_date, updated_at)
                    values
                    (1, null, datetime('now'));
            ''')

            self.connection.commit()

    def read(self, key):
        cursor = self.connection.cursor()
        cursor.execute('''
            select {0} from cron where id = 1
        '''.format(key))
        result = cursor.fetchone()
        if result == None:
            return None

        return result[key]

    def write(self, key, value):
        cursor = self.connection.cursor()
        cursor.execute('''
            update cron
            set {0} = ?,
            updated_at = datetime('now')
            where id = 1
        '''.format(key), (value, ))
        
        self.connection.commit()
