import sqlite3

#estabelecer uma conexão
conexao = sqlite3.connect ("banco.db")

with open('schema.sql') as f:
    conexao.executescript(f.read())
    
conexao.close()