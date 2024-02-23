import random
import sqlite3


#Ao executar este arquivo ele vai limpar o banco e adicionar varias "pessoas" ao banco

try:
    banco = sqlite3.connect("Banco_funcionarios")
    cursor = banco.cursor()
except Exception as e:
    print(e)


cursor.execute("delete from funcionarios where 1=1")
for i in range(100):
    tnome = f"pessoa{i}"
    ano = random.randint(1800,2024)
    mes = random.randint(1,12)
    dia = random.randint(1,31)
    tnascimento = f"{ano}-{mes:02d}-{dia:02d}"
    tendereco = f"rua {i}"
    tcpf = f"123.456.789-{i:02d}"
    testado_civil = random.choice(["solteiro","viuvo","casado","solteira","viuva","casada"])
    insert_string = "insert into funcionarios(nome,nascimento,endereco,cpf,estado_civil) values(?,?,?,?,?)"
    values = (tnome, tnascimento, tendereco, tcpf, testado_civil)
    cursor.execute(insert_string, values)
    
banco.commit()
