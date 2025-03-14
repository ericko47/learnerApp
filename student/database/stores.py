
import sqlite3 as sql

class sdata():
    @staticmethod
    def learner():
        con = sql.connect('learnerapp.db')
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS student(
        Class_Group text,
        RegNo text,
        Password text
        )
        """)
        con.commit()
        con.close()
        return