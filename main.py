from fastapi import FastAPI, Query
from routers import conversoes, llm

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
)

app.include_router(conversoes.router)
app.include_router(llm.router)