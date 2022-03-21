from traceback import print_tb
from fastapi import FastAPI, Query, Path, Body, Header, HTTPException
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, HttpUrl
from fastapi.encoders import jsonable_encoder
from uuid import UUID


from json_utils import *

app = FastAPI()


# *********************************************************************************#
##################################### Produtos #####################################
# *********************************************************************************#


class ProductsIn(BaseModel):
    id_produto: Optional[int] = Field(None, ge=1)
    nome: str = Field(..., max_length=45)
    marca: Optional[str] = Field(None, max_length=45)
    preco: float
    categoria: str = Field(..., max_length=45)
    descricao: Optional[str] = Field(None, max_length=150)
    desconto: Optional[float] = Field(None, ge=0, le=1)

@app.get("/products/", tags=["Produto"])
async def get_products():
    data = read_data("produto")
    return {"produtos": data}


@app.get("/products/{id_produto}", tags=["Produto"])
async def get_products(
    *, 
    id_produto: int = Path(..., title="The ID of the product to get", ge=1)
):

    id_exists = check_id("produto", "id_produto", id_produto)

    if not id_exists:
        raise HTTPException(status_code=404, detail="Product not found")
    else:
        data = read_data("produto")
        filtered = list(filter(lambda x: x["id_produto"] == id_produto, data))[0]
        return {"produto": filtered}


@app.post("/products/create/", tags=["Produto"])
async def create_product_by_id(
    product: ProductsIn= Body(
        ...,
        examples={
            "normal": {
                "summary": "A normal example",
                "description": "A **normal** request to create a product.",
                "value": {
                    "nome": "string",
                    "marca": "string",
                    "preco": 10.50,
                    "categoria": "string",
                    "descricao": "string",
                    "desconto": 0.2,
                },
            }
        })
):
    product.id_produto = get_next_id("produto", "id_produto")
    json_produto = jsonable_encoder(product)
    create_data(json_produto, "produto")
    return {"message": "success"}


@app.post("/products/update/{id_produto}", tags=["Produto"])
async def update_product(
    *,
    id_produto: int = Path(..., title="The ID of the product to get", ge=1),
    product: ProductsIn= Body(
        ...,
        examples={
            "normal": {
                "summary": "A normal example",
                "description": "A **normal** request to update.",
                "value": {
                    "nome": "string",
                    "marca": "string",
                    "preco": 10.50,
                    "categoria": "string",
                    "descricao": "string",
                    "desconto": 0.2,
                },
            }
        })
):
    id_exists = check_id("produto", "id_produto", id_produto)

    if not id_exists:
        raise HTTPException(status_code=404, detail="Product not found")
    else:
        data = read_data("produto")
        filtered = list(filter(lambda x: x["id_produto"] == id_produto, data))[0]
        json_filtered = jsonable_encoder(filtered)
        
        product.id_produto = json_filtered['id_produto']
        json_produto = jsonable_encoder(product)
        update_data("produto", ["id_produto"], [id_produto], json_produto)

        return {"message": "success"}


@app.delete("/products/delete/{id_produto}", tags=["Produto"])
async def delete_product(
    *,
    id_produto: int = Path(..., title="The ID of the product to get", ge=1),
):
    id_exists = check_id("produto", "id_produto", id_produto)

    if not id_exists:
        raise HTTPException(status_code=404, detail="Product not found")
    else:
        delete_data("produto", ["id_produto"], [id_produto])
    
        return {"message": "success"}


# *********************************************************************************#
##################################### Carrinho #####################################
# *********************************************************************************#

class CartIn(BaseModel):
    id_carrinho: Optional[int] = Field(None, ge=1)
    fk_id_usuario: Optional[int] = Field(None, ge=1)


# Puxa lista de todos os carrinhos e seus donos
@app.get("/cart/", tags=["Carrinho"])
async def get_all_carts():
    data = read_data("carrinho")
    return {"carrinho": data}

@app.post("/cart/create/", tags=["Carrinho"])
async def create_cart(
    cart: CartIn= Body(
        ...,
        examples={
            "normal": {
                "summary": "A normal example",
                "description": "A **normal** request to create a product.",
                "value": {
                    "id_usuario": None,
                },
            }
        }
        )
):
    cart.id_carrinho = get_next_id("carrinho", "id_carrinho")
    json_carrinho = jsonable_encoder(cart)
    create_data(json_carrinho, "carrinho")
    return {"message": "success"}

@app.delete("/cart/delete/{id_carrinho}", tags=["Carrinho"])
async def delete_cart(
    *,
    id_carrinho: int = Path(..., title="The ID of the cart to get", ge=1)
):
    id_exists = check_id("carrinho", "id_carrinho", id_carrinho)

    if not id_exists:
        raise HTTPException(status_code=404, detail="Cart not found")
    else:
        delete_data("carrinho_produto", ["fk_id_carrinho"], [id_carrinho])
        delete_data("carrinho", ["id_carrinho"], [id_carrinho])

        return {"message": "success"}



# *********************************************************************************#
################################ Produto Carrinho ##################################
# *********************************************************************************#

class Cart_productIn(BaseModel):
    fk_id_carrinho: Optional[int] = Field(None, ge=1)
    fk_id_produto: Optional[int] = Field(None, ge=1)
    quantidade: Optional[int] = Field(None, ge=1)

# Se o id_carrinho existe em "carrinho", puxamos seus dados em "carrinho_produto"
@app.get("/cart/{id_carrinho}", tags=["Carrinho-produto"])
async def get_cart_products(
    *, 
    id_carrinho: int = Path(..., title="The ID of the cart to get", ge=1)
):

    id_exists = check_id("carrinho", "id_carrinho", id_carrinho)

    if not id_exists:
        raise HTTPException(status_code=404, detail="Cart not found")
    else:
        data = read_data("carrinho_produto")
        filtered = list(filter(lambda x: x["fk_id_carrinho"] == id_carrinho, data))
        return {"carrinho_produto": filtered}




@app.post("/cart/addprod/{id_carrinho}", tags=["Carrinho-produto"])
async def update_cart_product(
    *,
    id_carrinho: int = Path(..., title="The ID of the cart to get", ge=1),
    cart: Cart_productIn= Body(
        ...,
        examples={
            "normal": {
                "summary": "A normal example",
                "description": "A **normal** request to create a product.",
                "value": {
                    "fk_id_produto": 1,
                    "quantidade": 5
                },
            }
        })
):
    id_exists = check_id("carrinho", "id_carrinho", id_carrinho)

    if not id_exists:
        raise HTTPException(status_code=404, detail="Cart not found")
    else:
        json_carrinho = jsonable_encoder(cart)
        create_data(json_carrinho, "carrinho_produto")
        
        return {"message": "success"}


@app.delete("/cart/deleteprod/{id_carrinho}/{id_produto}", tags=["Carrinho-produto"])
async def delete_cart_product(
    *,
    id_carrinho: int = Path(..., title="The ID of the cart to get", ge=1),
    id_produto: int = Path(..., title="The ID of the product to get", ge=1)

):
    id_exists = check_id("carrinho", "id_carrinho", id_carrinho)

    if not id_exists:
        raise HTTPException(status_code=404, detail="Cart not found")
    else:
        delete_data("carrinho_produto", ["fk_id_carrinho", "fk_id_produto"], [id_carrinho, id_produto])

        return {"message": "success"}






