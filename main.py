from fastapi import FastAPI, Query
from utils import (
    obter_logger_e_configuracao, 
    converter_pdf_para_texto_pyPDF2, 
    converter_pdf_para_texto_pdfplumber,
    converter_pdf_para_texto_pymupdf,
    converter_pdf_para_texto_pdf2image,
    resumir_pdf_groq,
    resumir_pdf_openai,
    manipular_pdf_openai
    )
from models import ModeloOpenAi, NomeGrupo



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
    "/v1/convert_pdf_text_pyPDF2", 
    summary="Converte um PDF para texto",
    description="Extrai o texto de um arquivo PDF usando a biblioteca PyPDF2 do Python.",
    tags=[NomeGrupo.conversao],
)
def converter_pdf(caminho_pdf: str):
    texto_extraido = converter_pdf_para_texto_pyPDF2(caminho_pdf)
    return {"texto": texto_extraido}


@app.post(
    "/v1/convert_pdf_text_pdfpluber", 
    summary="Converte um PDF para texto usando o PDFPlumber",
    description="Extrai o texto de um arquivo PDF usando a biblioteca PDFPlumber do Python.",
    tags=[NomeGrupo.conversao],
)
def converter_pdf(caminho_pdf: str):
    texto_extraido = converter_pdf_para_texto_pdfplumber(caminho_pdf)
    return {"texto": texto_extraido}


@app.post(
    "/v1/convert_pdf_text_fitz", 
    summary="Converte um PDF para texto usando o pymupdf (ou fitz)",
    description="Extrai o texto de um arquivo PDF usando a biblioteca pymupdf (ou fitz) do Python.",
    tags=[NomeGrupo.conversao], 
)
def converter_pdf(caminho_pdf: str):
    texto_extraido = converter_pdf_para_texto_pymupdf(caminho_pdf)
    return {"texto": texto_extraido}


@app.post(
    "/v1/convert_pdf_ocr_text_pdf2image", 
    summary="Converte um PDF escaneado (OCR) para texto usando o pdf2image",
    description="Extrai o texto de um arquivo PDF escaneado (OCR) usando a biblioteca pdf2image do Python."
    "Para funcionar, é necessário ter o Tesseract instalado e configurado no sistema operacional, além "
    "do diretório poppler baixado na máquina. É necessário também a inclusão dos caminhos do poppler e do Tesseract "
    "nas variáveis de ambiente/sistema.",
    tags=[NomeGrupo.conversao],
)
def converter_pdf(caminho_pdf: str):
    texto_extraido = converter_pdf_para_texto_pdf2image(caminho_pdf)
    return {"texto": texto_extraido}


# Utilizando a Groq como LLM
@app.post(
    "/v1/pdf_resumo_groq", 
    summary="Gera um resumo do PDF utilizando Groq como LLM - modelo llama-3.1-8b-instant.",
    description="Extrai o texto do PDF e produz um resumo estruturado em tópicos utilizando a Groq como LLM - modelo llama-3.1-8b-instant.",
    tags=[NomeGrupo.llm],
)
def resumir_pdf(caminho_pdf: str):
    resultado = resumir_pdf_groq(caminho_pdf)
    return resultado


@app.post(
    "/v1/pdf_resumo_openai", 
    summary="Gera um resumo do PDF utilizando a OpenAI como LLM - modelo gpt-4o-mini.",
    description="Extrai o texto do PDF e produz um resumo estruturado em tópicos utilizando a OpenaAI como LLM - modelo gpt-4o-mini.",
    tags=[NomeGrupo.llm],
)
def resumir_pdf(caminho_pdf: str):
    resultado = resumir_pdf_openai(caminho_pdf)
    return resultado

@app.post(
    "/v1/pdf_manipulacao_openai", 
    summary="Manipula um PDF utilizando a OpenAI como LLM.",
    description="Executa qualquer tarefa de manipulação de PDF, conforme parâmetros informados pelo usuário, utilizando a OpenaAI como LLM.",
    tags=[NomeGrupo.llm],
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

