from fastapi import FastAPI, Depends
from routers import conversoes, llm
from utils import commom_verificacao_api_token

description = """
    API desenvolvida para o trabalho final da disciplina de API.
    Desenvolvido por Guilherme Lemes, Raphael Rodrigues e Thiago Santos, 
    não obstante o código estar concentrado em uma única conta no github."""

app = FastAPI(
    title="API - Projeto Final",
    description=description,
    version="0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Raphael Rodrigues",
        "url": "http://github.com/raphaelrsantos/",
        "email": "raphaelrsantos@gmail.com",
    },
    dependencies=[
        Depends(commom_verificacao_api_token)
    ],  # com essa linha, o token é verificado em todas as requisições, ja que busca a função commom_verificacao_api_token
)

app.include_router(conversoes.router)
app.include_router(llm.router)