from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
import pypyodbc as odbc
import sqlite3

app = FastAPI()
templates = Jinja2Templates(directory="templates")

try:
    banco = sqlite3.connect("Banco_funcionarios")
    cursor = banco.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS funcionarios (
            id integer primary key,
            nome varchar(75),
            nascimento date,
            endereco varchar(150),
            cpf varchar(14) unique,
            estado_civil varchar(10)
        )""")
except Exception as e:
    print(e)


@app.get("/", response_class=HTMLResponse)
async def Home(request: Request):

    try:
        cursor.execute("SELECT * FROM funcionarios")
        pessoas = cursor.fetchall()
    except Exception as e:
        print(e)
    
    return templates.TemplateResponse("index.html", {"request": request, "pessoas": pessoas})


@app.post("/adicionar_pessoa")
async def adicionar_pessoa(request: Request):
    #id
    #nome
    #nascimento
    #endereço
    #cpf
    #estado_civil

    form = await request.form()
    nome = form["nome"]
    nascimento = form["nascimento"]
    endereco = form["endereco"]
    cpf = form["cpf"]
    estado_civil = form["estadoCivil"]
    try:
        insert_string = "INSERT INTO funcionarios (nome, nascimento, endereco, cpf, estado_civil) VALUES (?, ?, ?, ?, ?)"
        insert_values = (nome, nascimento, endereco, cpf, estado_civil)

        cursor.execute(insert_string, insert_values)
        banco.commit()
        print("Pessoa adicionada com sucesso")
        redirect_response = f"""
            <html>
                <head>
                    <meta http-equiv="refresh" content="0; url=/">
                </head>
                <body>
                    <script>
                        alert("Pessoa adicionada com sucesso!");
                    </script>
                </body>
            </html>
        """
        return HTMLResponse(content=redirect_response)
        
    except Exception as e:
        print(e)
        return {"error": "Erro ao adicionar pessoa", "message": e}
    
    
@app.post("/deletar_cadastro")
async def deletar_cadastro(request: Request):

    form = await request.form()
    print(form)
    id = form["id"]
    
    try:
        string = "delete from funcionarios where id = ?"

        cursor.execute(string, id)
        banco.commit()
        print("Pessoa removida com sucesso")
        redirect_response = f"""
            <html>
                <head>
                    <meta http-equiv="refresh" content="0; url=/">
                </head>
                <body>
                    <script>
                        alert("Pessoa removida com sucesso!");
                    </script>
                </body>
            </html>
        """
        return HTMLResponse(content=redirect_response)
        
    except Exception as e:
        print(e)
        return {"error": "Erro ao remover pessoa", "message": e}
    
@app.get("/pesquisar")
async def pesquisar(request: Request, coluna: str, valorPesquisa: str):
    try:
        string = f"select * from funcionarios where {coluna} = ?"

        cursor.execute(string, (valorPesquisa,))
        pessoas = cursor.fetchall()
        print(pessoas)
        return templates.TemplateResponse("index.html", {"request": request, "pessoas": pessoas})
        
    except Exception as e:
        print(e)
        return {"error": "Erro ao pesquisar", "message": e}

    

    
    
