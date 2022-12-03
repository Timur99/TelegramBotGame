import sqlite3

conn = sqlite3.connect('sqlbase/base.db', check_same_thread=False)
cursor = conn.cursor()


def db_table_val(username: str, task: str):
	cursor.execute('INSERT INTO taskbase (username, task) VALUES (?, ?)', (username, task))
	conn.commit()


