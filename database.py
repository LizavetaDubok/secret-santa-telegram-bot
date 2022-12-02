import sqlite3


class DataBase:
    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def add_participant(self, chat_id):
        with self.connection:
            return self.cursor.execute('INSERT INTO "participants" ("chat_id") VALUES (?)', (chat_id, ))

    def check_participant(self, chat_id):
        with self.connection:
            return bool(len((self.cursor.execute('SELECT * FROM "participants" WHERE "chat_id" = ?',
                                                 (chat_id, ))).fetchmany(1)))

    def delete_participant(self, chat_id):
        with self.connection:
            return self.cursor.execute('DELETE FROM "participants" WHERE "chat_id" = ?', (chat_id, ))

    def set_participant_wishes(self, chat_id, wishes):
        with self.connection:
            return self.cursor.execute('UPDATE "participants" SET "wishes" = ? WHERE "chat_id" = ?', (wishes, chat_id))

    def get_chat_id_by_id(self, id_):
        return self.cursor.execute('SELECT "chat_id" FROM "participants" WHERE "id" = ?',
                                   (id_,)).fetchone()[0]

    def set_santa(self, id, santa_id):
        with self.connection:
            return self.cursor.execute('UPDATE "participants" SET "santa_id" = ? WHERE "id" = ?',
                                       (santa_id, id))

    def make_dummy_matches(self):
        with self.connection:
            return self.cursor.execute('UPDATE "participants" SET "santa_id" = "chat_id"', ())

    def get_participants_id(self):
        with self.connection:
            result = list(zip(*self.cursor.execute('SELECT "id" FROM "participants"', ()).fetchall()))
            return result[0]

    def get_matches(self):
        with self.connection:
            return self.cursor.execute('SELECT "chat_id", "santa_id" FROM "participants"', ()).fetchall()

    def get_participants(self):
        with self.connection:
            result = list(zip(*self.cursor.execute('SELECT "chat_id" FROM "participants"', ()).fetchall()))
            return result[0]

    def get_participant_wishes(self, chat_id):
        with self.connection:
            return self.cursor.execute('SELECT "wishes" FROM "participants" WHERE "chat_id" = ?',
                                       (chat_id,)).fetchone()[0]

    def get_participant_ward(self, chat_id):
        with self.connection:
            return self.cursor.execute('SELECT "chat_id" FROM "participants" WHERE "santa_id" = ?',
                                       (chat_id,)).fetchone()[0]

    def get_participant_santa(self, chat_id):
        with self.connection:
            return self.cursor.execute('SELECT "santa_id" FROM "participants" WHERE "chat_id" = ?',
                                       (chat_id,)).fetchone()[0]

