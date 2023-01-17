import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO post (titulo, conteudo, categoria, usuario) VALUES (?, ?, ?, ?)",
            ('First Post', 'Content for the first post', 'teste', 'teste@gmail.com')
            )


connection.commit()
connection.close()