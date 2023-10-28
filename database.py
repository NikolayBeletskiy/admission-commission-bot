import sqlite3


class Exams:
    @staticmethod
    def create(subject, date):
        with sqlite3.connect('commission.db') as db:
            cursor = db.cursor()
            cursor.execute(f"INSERT INTO exams (subject, date) VALUES {(subject, date)}")
            db.commit()

    @staticmethod
    def read(id) -> tuple:
        with sqlite3.connect('commission.db') as db:
            cursor = db.cursor()
            cursor.execute(f"SELECT * FROM exams WHERE rowid = {id}")
            return cursor.fetchone()

    @staticmethod
    def read_all() ->list[tuple]:
        with sqlite3.connect('commission.db') as db:
            cursor = db.cursor()
            cursor.execute(f"SELECT * FROM exams")
            return cursor.fetchall()

    @staticmethod
    def delete(id):
        with sqlite3.connect('commission.db') as db:
            cursor = db.cursor()
            cursor.execute(f"DELETE FROM exams WHERE rowid = {id}")
            db.commit()