import sqlite3

#insert

conn = sqlite3.connect('banco.db')

SQL = "insert into users (nome) values (?)"

nome = 'Livia'
conn.execute(SQL, (nome,))
conn.commit()

conn.close()