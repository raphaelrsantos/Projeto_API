from fastapi import FastAPI
from utils import executar_prompt
from utils import obter_logger_e_configuracao


logger = obter_logger_e_configuracao()


description = """
    API desenvolvida para o trabalho final da disciplina de API.
    Trabalho desenvolvido por Guilherme Lemes, Raphael Rodrigues e Thiago Santos."""

app = FastAPI(
    title="API - Projeto Final",
    description=description,
    version="0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Guilherme Lemes, Raphael Rodrigues, Thiago Santos",
        "url": "http://github.com/raphaelrsantos/",
        "email": "grupo14@EMAIL.COM",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },  
)


@app.post(
    "/v1/gerar_historia",
    summary="Gera uma história sobre o tema informado por parâmetro",
    description="Gera uma história em português brasileiro sobre um tema específico usando a API Groq.",
)
def gerar_historia(tema: str):
    logger.info(f"Tema informado: {tema}")

    historia = executar_prompt(tema)
    logger.info("História gerada com sucesso!")
    ## logger.info(f"História gerada: {historia}")

    return {"historia": historia}
