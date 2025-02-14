from fastapi import FastAPI
from utils import (
    obter_logger_e_configuracao, 
    converter_pdf_para_texto_pyPDF2, 
    resumir_pdf_llm
)


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
    "/v1/converter_pdf_para_texto_pyPDF2", 
    summary="Converte um PDF para texto",
    description="Extrai o texto de um arquivo PDF usando PyPDF2."
)
def converter_pdf(caminho_pdf: str):
    texto_extraido = converter_pdf_para_texto_pyPDF2(caminho_pdf)
    return {"texto": texto_extraido}


@app.post(
    "/v1/converter_pdf_xml_resumo", 
    summary="Converte um PDF para XML e gera um resumo didático",
    description="Extrai o texto do PDF, converte para um formato XML e produz um resumo estruturado em tópicos utilizando a LLM (Groq)."
)
def converter_pdf_xml_resumo(caminho_pdf: str):
    resultado = resumir_pdf_llm(caminho_pdf)
    return resultado
