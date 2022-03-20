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
