# Resumo do Tutorial Fast API

Comando do terminal para rodar:
```python
# only use --reload for development
uvicorn main:app --reload
```

No FastAPI Swagger:
```python
http://127.0.0.1:8000/docs
```

### Exemplo:
```python
from fastapi import FastAPI

app = FastAPI()

# @ = decorator
# .get - define que a função abaixo vai usar esse método HTTP
@app.get("/")
async def root():
    return {"message": "Hello World"}
# Se a função não precisar retorno de ninguém usar async def
```

Métodos HTTP:
- POST
- GET
- DELETE
- PUT

Outros:
- OPTIONS
- HEAD
- PATCH
- TRACE

### Exemplo 2
```python
from fastapi import FastAPI

app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

# query parameters
# function parameters that are not part of the path parameters
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]
```

## Declarando a classe de dados

FastAPI vai:
- Ler o body o corpo do request como JSON
- Converter os tipos correspondentes
- Validar os dados
- Dar os dados recebidos
- Gerar o Schema JSON de definições