
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pypyodbc as odbc

app = FastAPI()
templates = Jinja2Templates(directory="templates")

DRIVER_NAME = 'SQL SERVER'
SERVER_NAME = 'DESKTOP-NPPOSVU' #select @@SERVERNAME
DATABASE_NAME = 'empresa'

connection_string = f"""
    DRIVER={{{DRIVER_NAME}}};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trust_Connection=yes;
"""

try:
    conn = odbc.connect(connection_string)
except Exception as e:
    print(e)

@app.get("/", response_class=HTMLResponse)
async def Home(request: Request):

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM pessoas")
        pessoas = cursor.fetchall()
        print(pessoas)
        print("Operação bem-sucedida")
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
    id = form["id"]
    nome = form["nome"]
    nascimento = form["nascimento"]
    endereco = form["endereco"]
    cpf = form["cpf"]
    estado_civil = form["estadoCivil"]
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO pessoas (id, nome, nascimento, endereco, cpf, estado_civil) VALUES (?, ?, ?, ?, ?, ?)", (id, nome, nascimento, endereco, cpf, estado_civil))
        conn.commit()
        print("Pessoa adicionada com sucesso")
    except Exception as e:
        print(e)
        return {e}
    return {"message": "Pessoa adicionada com sucesso"}
