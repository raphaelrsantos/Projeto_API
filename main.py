from fastapi import FastAPI, Query
from utils import (
    obter_logger_e_configuracao, 
    converter_pdf_para_texto_pyPDF2, 
    resumir_pdf_groq,
    resumir_pdf_openai,
    manipular_pdf_openai
    )
from models import ModeloOpenAi 



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
    summary="Gera um resumo do PDF utilizando Groq como LLM - modelo llama-3.1-8b-instant.",
    description="Extrai o texto do PDF e produz um resumo estruturado em tópicos utilizando a Groq como LLM - modelo llama-3.1-8b-instant.",
    tags=["Manipulação de PDFs"],
)
def resumir_pdf(caminho_pdf: str):
    resultado = resumir_pdf_groq(caminho_pdf)
    return resultado


@app.post(
    "/v1/pdf_resumo_openai", 
    summary="Gera um resumo do PDF utilizando a OpenAI como LLM - modelo gpt-4o-mini.",
    description="Extrai o texto do PDF e produz um resumo estruturado em tópicos utilizando a OpenaAI como LLM - modelo gpt-4o-mini.",
    tags=["Manipulação de PDFs"],
)
def resumir_pdf(caminho_pdf: str):
    resultado = resumir_pdf_openai(caminho_pdf)
    return resultado

@app.post(
    "/v1/pdf_manipulacao_openai", 
    summary="Manipula um PDF utilizando a OpenAI como LLM.",
    description="Executa qualquer tarefa de manipulação de PDF, conforme parâmetros informados pelo usuário, utilizando a OpenaAI como LLM.",
    tags=["Manipulação de PDFs"],
)
def manipular_pdf(
    # caminho_pdf: str = fr"C:\Users\rapha\Downloads\15_11_25_482_32_Licen_a_para_tratamento_de_doen_a_em_pessoa_da_fam_lia_efetivo.pdf",
    caminho_pdf: str = Query(..., title="Caminho para o arquivo PDF", description="O caminho para o arquivo PDF."),
    persona: str = Query("Você é um renomado professor com bastante experiência em montagem de esquemas e "
                         "resumos extremamente atrativos para seus alunos.", 
                         title="Persona", 
                         description="Personagem que a IA se tornará para execução da tarefa.", 
                         ),
    prompt: str = Query("Faça um resumo no modelo perguntas e respostas do texto contido no arquivo.", 
                         title="Prompt", 
                         description="Prompt a ser executado pelaIA.", 
                         ), 
    modelo: ModeloOpenAi = ModeloOpenAi.gpt_4o_mini  
):
    resultado = manipular_pdf_openai(caminho_pdf, persona, prompt, modelo.value)
    return resultado

