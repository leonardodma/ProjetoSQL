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


class ProductsInOptional(BaseModel):
    id_produto: Optional[int] = Field(None, ge=1)
    nome: Optional[str] = Field(None, max_length=45)
    marca: Optional[str] = Field(None, max_length=45)
    preco: Optional[float]
    categoria: Optional[str] = Field(None, max_length=45)
    descricao: Optional[str] = Field(None, max_length=150)
    desconto: Optional[float] = Field(None, ge=0, le=1)


@app.get("/products/", tags=["Produto"])
async def get_all_products():
    data = read_data("produto")
    return {"produtos": data}


@app.get("/products/{id_produto}", tags=["Produto"])
async def get_product(
    *,
    id_produto: int = Path(..., title="The ID of the product to get", ge=1)
):

    id_exists = check_id("produto", "id_produto", id_produto)

    if not id_exists:
        raise HTTPException(status_code=404, detail="Product not found")
    else:
        data = read_data("produto")
        filtered = list(
            filter(lambda x: x["id_produto"] == id_produto, data))[0]
        return {"produto": filtered}


# Create itens
@app.post("/products/", tags=["Produto"])
async def create_product(
    product: ProductsIn = Body(
        ...,
        examples={
            "normal": {
                "summary": "Normal example",
                "description": "A **normal** request to create a product.",
                "value": {
                    "nome": "string",
                    "marca": "string",
                    "preco": 10.50,
                    "categoria": "string",
                    "descricao": "string",
                    "desconto": 0.2,
                },
            },
            "mandatory": {
                "summary": "Mandatory example",
                "description": "A **mandatory** request to create a product has to set these parameters.",
                "value": {
                    "nome": "string",
                    "preco": 10.50,
                    "categoria": "string"
                },
            }
        })
):
    product.id_produto = get_next_id("produto", "id_produto")
    json_produto = jsonable_encoder(product)
    create_data(json_produto, "produto")
    return {"message": "success"}


# Replace itens
@app.patch("/products/{id_produto}", tags=["Produto"])
async def replace_product(
    *,
    id_produto: int = Path(..., title="The ID of the product to get", ge=1),
    product: ProductsIn = Body(
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
            },
            "mandatory": {
                "summary": "Mandatory example",
                "description": "A **mandatory** request to create a product has to set these parameters.",
                "value": {
                    "nome": "string",
                    "preco": 10.50,
                    "categoria": "string"
                },
            }
        })
):
    id_exists = check_id("produto", "id_produto", id_produto)

    if not id_exists:
        raise HTTPException(status_code=404, detail="Product not found")
    else:
        data = read_data("produto")
        filtered = list(
            filter(lambda x: x["id_produto"] == id_produto, data))[0]
        json_filtered = jsonable_encoder(filtered)

        product.id_produto = json_filtered['id_produto']
        json_produto = jsonable_encoder(product)
        update_data("produto", ["id_produto"], [id_produto], json_produto)

        return {"message": "success"}


# Update itens
@app.put("/products/{id_produto}", tags=["Produto"])
async def update_product(
    *,
    id_produto: int = Path(..., title="The ID of the product to get", ge=1),
    product: ProductsInOptional = Body(
        ...,
        examples={
            "normal": {
                "summary": "A normal example",
                "description": "A **normal** request to update. Put the field that you want to update.",
                "value": {
                    "preco": 15.00
                },
            }
        })
):
    id_exists = check_id("produto", "id_produto", id_produto)

    if not id_exists:
        raise HTTPException(status_code=404, detail="Product not found")
    else:
        data = read_data("produto")
        filtered = list(
            filter(lambda x: x["id_produto"] == id_produto, data))[0]
        json_filtered = jsonable_encoder(filtered)
        json_produto = jsonable_encoder(product)

        for key, value in json_produto.items():
            if value != None:
                json_filtered[key] = value

        update_data("produto", ["id_produto"], [id_produto], json_filtered)

        return {"message": "success"}


# Delete data
@app.delete("/products/{id_produto}", tags=["Produto"])
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


@app.post("/cart/", tags=["Carrinho"])
async def create_cart(
    cart: CartIn = Body(
        ...,
        examples={
            "normal": {
                "summary": "A normal example",
                "description": "A **normal** request to create a cart.",
                "value": {
                    "id_carrinho": 1,
                    "fk_id_usuario": 1,
                },
            },
            "mandatory": {
                "summary": "A mandatory example",
                "description": "A **mandatory** request to create a cart doesn't have any mandatory parameters.",
                "value": {
                },
            }
        }
    )
):
    cart.id_carrinho = get_next_id("carrinho", "id_carrinho")
    json_carrinho = jsonable_encoder(cart)
    create_data(json_carrinho, "carrinho")
    return {"message": "success"}


@app.delete("/cart/{id_carrinho}", tags=["Carrinho"])
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

class CartProductIn(BaseModel):
    fk_id_carrinho: Optional[int] = Field(None, ge=1)
    fk_id_produto: Optional[int] = Field(None, ge=1)
    quantidade: int = Field(..., ge=1)

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
        filtered = list(
            filter(lambda x: x["fk_id_carrinho"] == id_carrinho, data))
        return {"carrinho_produto": filtered}


@app.put("/cart/{id_carrinho}/{id_produto}", tags=["Carrinho-produto"])
async def update_cart_product(
    *,
    id_carrinho: int = Path(..., title="The ID of the cart to get", ge=1),
    id_produto: int = Path(..., title="The ID of the product to get", ge=1),
    cart: CartProductIn = Body(
        ...,
        examples={
            "normal": {
                "summary": "A normal example",
                "description": "A **normal** request to update a quantity of a product in a cart.",
                "value": {
                    "quantidade": 5
                },
            }
        })
):
    id_exists = check_id("carrinho", "id_carrinho", id_carrinho)

    if not id_exists:
        raise HTTPException(status_code=404, detail="Cart not found")
    else:
        data = read_data("carrinho_produto")
        filtered = list(
            filter(lambda x: x["fk_id_carrinho"] == id_carrinho, data))

        for item in filtered:
            if item["fk_id_produto"] == id_produto:
                json_carrinho = jsonable_encoder(cart)

                for key, value in json_carrinho.items():
                    if value != None:
                        item[key] = value
                        update_data("carrinho_produto", ["fk_id_carrinho", "fk_id_produto"], [id_carrinho, id_produto], item)

        return {"message": "success"}


@app.delete("/cart/{id_carrinho}/{id_produto}", tags=["Carrinho-produto"])
async def delete_cart_product(
    *,
    id_carrinho: int = Path(..., title="The ID of the cart to get", ge=1),
    id_produto: int = Path(..., title="The ID of the product to get", ge=1)

):
    id_exists = check_id("carrinho", "id_carrinho", id_carrinho)

    if not id_exists:
        raise HTTPException(status_code=404, detail="Cart not found")
    else:
        delete_data("carrinho_produto", ["fk_id_carrinho", "fk_id_produto"], [
                    id_carrinho, id_produto])

        return {"message": "success"}
