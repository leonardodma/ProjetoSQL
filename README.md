# ProjetoSQL - Fase 1
O projeto consiste no desenvolvimento de um microsserviço CRUD em API REST utilizando um novo framework Web chamado FastAPI. Na fase 1 do projeto criamos um esquema de carrinho de compras, onde o usuário pode criar e deletar seu carrinho, adicionar e remover produtos, tendo também a possibilidade de criar um produto, consultar inventário de produtos, alterar produto, remover produto do
inventário.

### Instalação e execução
Insira os seguintes comandos em um Prompt com Python 3.6+ instalado:

```
pip install fastapi
```

Instalação do ASGI server:

```
pip install "uvicorn[standard]"
```

Para rodar nossa aplicação:

```
python -m uvicorn main:app --reload
```
Acesse  [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) para fazer o teste da aplicação!

## Feedback pré-entrega:
- [X] Consertar a documentação e os exemplos
- [] Criar o update corretamente, hoje temos o patch