from fastapi import FastAPI
from utils import (
    obter_logger_e_configuracao, 
    converter_pdf_para_texto_pyPDF2, 
    resumir_pdf_groq,
    resumir_pdf_openai
)


logger = obter_logger_e_configuracao()


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

@app.post(
    "/v1/converter_pdf_para_texto_pyPDF2", 
    summary="Converte um PDF para texto",
    description="Extrai o texto de um arquivo PDF usando a biblioteca PyPDF2 do Python.",
    tags=["Conversão de arquivos"],
    
)
def converter_pdf(caminho_pdf: str):
    texto_extraido = converter_pdf_para_texto_pyPDF2(caminho_pdf)
    return {"texto": texto_extraido}


@app.post(
    "/v1/pdf_resumo_groq", 
    summary="Gera um resumo do PDF utilizando Groq como LLM.",
    description="Extrai o texto do PDF e produz um resumo estruturado em tópicos utilizando a Groq como LLM.",
    tags=["Manipulação de PDFs"],
)
def resumir_pdf(caminho_pdf: str):
    resultado = resumir_pdf_groq(caminho_pdf)
    return resultado


@app.post(
    "/v1/pdf_resumo_openai", 
    summary="Gera um resumo do PDF utilizando a OpenAI como LLM.",
    description="Extrai o texto do PDF e produz um resumo estruturado em tópicos utilizando a OpenaAI como LLM.",
    tags=["Manipulação de PDFs"],
)
def resumir_pdf(caminho_pdf: str):
    resultado = resumir_pdf_openai(caminho_pdf)
    return resultado
