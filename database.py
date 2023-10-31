import sqlite3


class DataBase:
    def __init__(self, database: str):
        self.database = database

    def __do(self, command: str):
        with sqlite3.connect(self.database) as db:
            cursor = db.cursor()
            cursor.execute(command)
            db.commit()
            return cursor

    def execute(self, command: str):
        self.__do(command)

    def select(self, command):
        return self.__do(command).fetchall()

    def select_one(self, command):
        return self.__do(command).fetchone()


db = DataBase('commission.db')


class Exams:
    @staticmethod
    def create(subject, date):
        db.execute(f"INSERT INTO exams (subject, date) VALUES {(subject, date)}")

    @staticmethod
    def read(id) -> tuple:
        return db.select_one(f"SELECT * FROM exams WHERE rowid = {id}")

    @staticmethod
    def read_all() -> list[tuple]:
        return db.select(f"SELECT * FROM exams")

    @staticmethod
    def delete(id):
        db.execute(f"DELETE FROM exams WHERE rowid = {id}")


class Specialties:
    @staticmethod
    def create(id, name: str, subject1: str, subject2: str, subject3: str):
        values = (id, name, subject1, subject2, subject3)
        db.execute(f"INSERT INTO specialties (id, name, subject1, subject2, subject3) VALUES {values}")

    @staticmethod
    def read(id) -> tuple:
        return db.select_one(f"SELECT * FROM specialties WHERE id = {id}")

    @staticmethod
    def read_all() -> list[tuple]:
        return db.select(f"SELECT * FROM specialties")

    @staticmethod
    def delete(id):
        db.execute(f"DELETE FROM specialties WHERE id = {id}")


class Applications:
    @staticmethod
    def create(student_id, speciality_id, point1, point2, point3):
        values = (student_id, speciality_id, point1, point2, point3)
        db.execute(f"INSERT INTO applications (student_id, speciality_id, point1, point2, point3) VALUES {values}")

    @staticmethod
    def read(id) -> tuple:
        return db.select_one(f"SELECT * FROM applications WHERE rowid = {id}")

    @staticmethod
    def read_all() -> list[tuple]:
        return db.select(f"SELECT * FROM applications")

    @staticmethod
    def delete(id):
        db.execute(f"DELETE FROM applications WHERE rowid = {id}")



