import sqlite3
import os
if not os.path.exists('agenda.db'):
    conexão = sqlite3.connect("agenda.db")
    cursor = conexão.cursor()
    sql=    'create table agenda('\
            'id integer primary key autoincrement,'\
            'nome varchar(50),'\
            'telefone varchar(20))' 

    cursor.execute(sql)
    # sentença SQL para inserir registros
    sql = 'insert into agenda (nome,telefone) values (?, ?)'
    registros = [('Maria','98821-8785'),
                 ('João','99876-5652')]
    for reg in registros:
        cursor.execute(sql,reg)
    
    # gravação no banco de dados. Sem commit, os dados não são gravados.
    conexão.commit()

    cursor.close()
    conexão.close()
    