import sqlite3 as sql

class dbs:
    @staticmethod
    def database1():
        con = sql.connect('school.db')
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS students(
        Stname text,
        Email text,
        YOB int,
        stid int,
        stPhone int,
        gender text,
        RegNo text,
        Course text,
        Department text,
        School text,
        Intake_Group text,
        Class_Group text
        )
        """)
        con.commit()
        con.close()
        return
    @staticmethod
    def learners():
        con = sql.connect('learnerapp.db')
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS student(
        Email text,
        RegNo text,
        Password text
        )
        """)
        con.commit()
        con.close()
        return

    @staticmethod
    def studentAcounts():
        con = sql.connect('school.db')
        cur = con.cursor()

        [exists] = cur.fetchone()

        con.commit()
        con.close()