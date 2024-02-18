import sqlite3


try:
    banco = sqlite3.connect("Banco_funcionarios")
    cursor = banco.cursor()
except Exception as e:
    print(e)
else:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS funcionarios (
            id integer primary key,
            nome varchar(75),
            nascimento date,
            endereco varchar(150),
            cpf varchar(14) unique,
            estado_civil varchar(10)
        )""")
    cursor.execute("insert into funcionarios (nome, nascimento, endereco, cpf, estado_civil) values ('pessoa1', '2000-01-03', 'casa n1234', '123.456.789-01', 'viuvo')")
    cursor.execute("insert into funcionarios (nome, nascimento, endereco, cpf, estado_civil) values ('pessoa2', '2000-01-03', 'casa n1235', '123.456.789-02', 'viuvo')")
    cursor.execute("insert into funcionarios (nome, nascimento, endereco, cpf, estado_civil) values ('pessoa3', '2000-01-03', 'casa n1236', '123.456.789-03', 'viuvo')")
    banco.commit()
    
    
    
