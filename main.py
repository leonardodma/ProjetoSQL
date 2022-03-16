from fastapi import FastAPI, Query, Path, Body, Header
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, HttpUrl
from fastapi.encoders import jsonable_encoder
from uuid import UUID

from json_utils import *

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Bem-vindo ao seu mercado!"}

# *********************************************************************************#
##################################### Produtos #####################################
# *********************************************************************************# 
class ProductsIn(BaseModel):
    id_produto: Optional[int] = Field(None, ge=1)
    nome: str = Field(..., max_length=45)
    marca: Optional[str] = Field(..., max_length=45)
    price: float
    categoria: str = Field(..., max_length=45)
    descricao: Optional[str] = Field(..., max_length=150)
    desconto: Optional[float] = Field(None, ge=0, le=1)


@app.get("/products/")
async def get_products():
    data = read_data("produto")
    return {"produtos": data}


@app.get("/products/{id_produto}")
async def get_products(*, id_produto: int = Path(..., title="The ID of the product to get", ge=1)):
    data = read_data("produto")
    filtered = list(filter(lambda x: x["id_produto"] == id_produto, data))[0]
    return {"produto": filtered}


@app.post("/products/create/")
async def update_product(product: ProductsIn):
    product.id_produto = get_next_id("produto", "id_produto")
    json_produto = jsonable_encoder(product)
    create_data(json_produto, "produto")
    return {"message": "success", "data": product}
