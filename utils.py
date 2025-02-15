import logging
from dotenv import load_dotenv
import openai
import os
from fastapi import HTTPException

load_dotenv()

def obter_logger_e_configuracao():
    """
    Configura o logger padrão para o nível de informação e formato especificado.

    Retorna:
        logging.Logger: Um objeto de logger com as configurações padrões.
    """
    logging.basicConfig(
        level=logging.INFO, format="[%(levelname)s] %(asctime)s - %(message)s"
    )
    logger = logging.getLogger("fastapi")
    return logger


def limpar_json_formatado(json_text):
    """
    Remove caracteres de markdown como ```json e ``` do início e fim do texto.
    """
    if json_text.startswith("```json"):
        json_text = json_text[7:]  # Remove o ```json inicial
    if json_text.endswith("```"):
        json_text = json_text[:-3]  # Remove o ``` final
    return json_text.strip()

import PyPDF2

def converter_pdf_para_texto_pyPDF2(caminho_pdf: str) -> str:
    """
    Converte um arquivo PDF para texto usando PyPDF2.

    Args:
        caminho_pdf (str): O caminho para o arquivo PDF.
    Returns:
        str: O texto extraído do arquivo PDF.
    """
    # Verifica se o arquivo existe
    if not os.path.exists(caminho_pdf):
        raise HTTPException(status_code=400, detail=f"Erro: O arquivo '{caminho_pdf}' não foi encontrado.")

    # Verifica se a extensão do arquivo é .pdf
    if not caminho_pdf.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Erro: O arquivo fornecido não é um PDF.")

    try:
        with open(caminho_pdf, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            texto = ""

            # Verifica se há páginas no PDF
            if not reader.pages:
                raise HTTPException(status_code=400, detail="Erro: O arquivo PDF está vazio ou corrompido.")

            for pagina in reader.pages:
                texto += pagina.extract_text() or ""  # Evita None

        return texto

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar o PDF: {str(e)}")


import pdfplumber

def converter_pdf_para_texto_pdfplumber(caminho_pdf: str) -> str:
    """
    Converte um arquivo PDF para texto usando pdfplumber.

    Args:
        caminho_pdf (str): O caminho para o arquivo PDF.
    Returns:
        str: O texto extraído do arquivo PDF.
    """

    # Verifica se o arquivo existe
    if not os.path.exists(caminho_pdf):
        raise HTTPException(status_code=400, detail=f"Erro: O arquivo '{caminho_pdf}' não foi encontrado.")

    # Verifica se a extensão do arquivo é .pdf
    if not caminho_pdf.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Erro: O arquivo fornecido não é um PDF.")

    try:
        texto = ""
        with pdfplumber.open(caminho_pdf) as pdf:
            # Verifica se o PDF contém páginas
            if not pdf.pages:
                raise HTTPException(status_code=400, detail="Erro: O arquivo PDF está vazio ou corrompido.")

            for pagina in pdf.pages:
                pagina_texto = pagina.extract_text()
                texto += pagina_texto + "\n" if pagina_texto else ""

        # Verifica se algum texto foi extraído
        if not texto.strip():
            raise HTTPException(status_code=400, detail="Erro: Nenhum texto foi extraído do PDF. O arquivo pode estar corrompido ou ser um PDF baseado em imagem.")

        return texto

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar o PDF: {str(e)}")


import fitz  # PyMuPDF

def converter_pdf_para_texto_pymupdf(caminho_pdf: str) -> str:
    """
    Converte um arquivo PDF para texto usando pymupdf (ou fitz).

    Args:
        caminho_pdf (str): O caminho para o arquivo PDF.
    Returns:
        str: O texto extraído do arquivo PDF.
    """

    # Verifica se o arquivo existe
    if not os.path.exists(caminho_pdf):
        raise HTTPException(status_code=400, detail=f"Erro: O arquivo '{caminho_pdf}' não foi encontrado.")

    # Verifica se a extensão do arquivo é .pdf
    if not caminho_pdf.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Erro: O arquivo fornecido não é um PDF.")

    try:
        doc = fitz.open(caminho_pdf)

        # Verifica se o PDF contém páginas
        if len(doc) == 0:
            raise HTTPException(status_code=400, detail="Erro: O arquivo PDF está vazio ou corrompido.")

        # Extrai o texto das páginas
        texto = "\n".join([pagina.get_text() for pagina in doc])

        # Verifica se algum texto foi extraído
        if not texto.strip():
            raise HTTPException(status_code=400, detail="Erro: Nenhum texto foi extraído do PDF. O arquivo pode estar corrompido ou ser um PDF baseado em imagem.")

        return texto

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar o PDF: {str(e)}")


from pdf2image import convert_from_path
import pytesseract

def converter_pdf_para_texto_pdf2image(caminho_pdf: str) -> str:
    """
    Converte um arquivo PDF digitalizado para texto usando pdf2image e OCR (pytesseract).

    Args:
        caminho_pdf (str): O caminho para o arquivo PDF.
    Returns:
        str: O texto extraído do arquivo PDF.
    """

    # Verifica se o arquivo existe
    if not os.path.exists(caminho_pdf):
        raise HTTPException(status_code=400, detail=f"Erro: O arquivo '{caminho_pdf}' não foi encontrado.")

    # Verifica se a extensão do arquivo é .pdf
    if not caminho_pdf.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Erro: O arquivo fornecido não é um PDF.")

    # Verifica se o Tesseract OCR está instalado
    if not pytesseract.pytesseract.tesseract_cmd:
        raise HTTPException(status_code=500, detail="Erro: O Tesseract OCR não está instalado ou não está no PATH.")

    try:
        # Converte PDF para imagens
        imagens = convert_from_path(caminho_pdf)

        # Verifica se o PDF gerou imagens
        if not imagens:
            raise HTTPException(status_code=400, detail="Erro: O PDF não contém imagens ou não pôde ser processado.")

        # Extrai o texto das imagens usando OCR
        texto = "\n".join([pytesseract.image_to_string(imagem) for imagem in imagens])

        # Verifica se algum texto foi extraído
        if not texto.strip():
            raise HTTPException(status_code=400, detail="Erro: Nenhum texto foi extraído do PDF. O arquivo pode estar corrompido ou não conter texto legível.")

        return texto

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar o PDF com OCR: {str(e)}")



# Utilizando a Groq como LLM

from groq import Groq, APIStatusError

def resumir_pdf_groq(caminho_pdf: str) -> dict:
    """
    Converte um PDF para um resumo estruturado utilizando Groq como LLM.

    Args:
        caminho_pdf (str): O caminho para o arquivo PDF.
    Returns:
        dict: Um dicionário contendo o resumo gerado pela LLM.
    """

    # Verifica se o arquivo existe
    if not os.path.exists(caminho_pdf):
        raise HTTPException(status_code=400, detail=f"Erro: O arquivo '{caminho_pdf}' não foi encontrado.")

    # Verifica se a extensão do arquivo é .pdf
    if not caminho_pdf.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Erro: O arquivo fornecido não é um PDF.")

    try:
        # Extrai o texto bruto do PDF
        texto_pdf = converter_pdf_para_texto_pyPDF2(caminho_pdf)

        if not texto_pdf.strip():
            raise HTTPException(status_code=400, detail="Erro: Nenhum texto foi extraído do PDF. O arquivo pode estar corrompido ou ser um PDF baseado em imagem.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao extrair texto do PDF: {str(e)}")

    # Cria o prompt para a LLM
    prompt = (
        "A partir do conteúdo txt extraído do PDF, crie um resumo didático. "
        "O resumo deve ser claro, objetivo e facilitar a compreensão para o usuário final. Coloque quebra de linhas no resumo. "
        "Não exicitar a palavra resumo no corpo da resposta\n\n"
        f"Texto extraído:\n{texto_pdf}"
    )

    # Obtém a chave da API do Groq
    api_key = os.getenv("GROQ_API_KEY")
    if api_key is None:
        raise HTTPException(status_code=500, detail="Erro: A chave da API 'GROQ_API_KEY' não foi encontrada no arquivo .env.")

    client = Groq(api_key=api_key)

    try:
        resposta = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
        )

        resumo = resposta.choices[0].message.content

        return {"resumo": resumo}

    except APIStatusError as e:
        error_str = str(e)
        if "rate_limit_exceeded" in error_str:
            raise HTTPException(status_code=429, detail="Erro: O request excedeu o limite de tokens por minuto. Reduza o tamanho da mensagem e tente novamente.")
        elif "authentication_error" in error_str:
            raise HTTPException(status_code=401, detail="Erro: Falha na autenticação com a API do Groq. Verifique sua chave de API.")
        else:
            raise HTTPException(status_code=500, detail=f"Erro ao processar o resumo com Groq: {str(e)}")


# Utilizando a OpenAi como LLM

import openai

def acessar_api_openai(content: str, prompt: str, modelo: str) -> str:
    """
    Acessa a API da OpenAI para processar uma conversa com base no conteúdo e no prompt.

    Args:
        content (str): Contexto do sistema para a IA.
        prompt (str): Entrada do usuário.
        modelo (str): Modelo da OpenAI a ser utilizado.

    Returns:
        str: A resposta formatada do modelo da OpenAI.
    """

    # Verifica se a chave da API está definida
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="Erro: A chave da API 'OPENAI_API_KEY' não foi encontrada. Verifique o arquivo .env.")

    try:
        # Inicializar o cliente da OpenAI
        client = openai.OpenAI(api_key=api_key)

        # Histórico da conversa
        conversation_history = [{"role": "system", "content": content}]

        # Adicionar a entrada ao histórico
        conversation_history.append({"role": "user", "content": prompt})

        # Enviar a requisição para a API da OpenAI
        completion = client.chat.completions.create(
            model=modelo,
            messages=conversation_history
        )

        # Extrair a resposta do modelo
        gpt_response = completion.choices[0].message.content

        # Limpar o JSON formatado (caso necessário)
        cleaned_json = limpar_json_formatado(gpt_response)

        return cleaned_json

    except APIStatusError as e:
        error_str = str(e)

        if "rate_limit_exceeded" in error_str:
            raise HTTPException(status_code=429, detail="Erro: O request excedeu o limite de tokens por minuto. Reduza o tamanho da mensagem e tente novamente.")
        elif "authentication_error" in error_str:
            raise HTTPException(status_code=401, detail="Erro: Falha na autenticação com a API da OpenAI. Verifique sua chave de API.")
        elif "model_not_found" in error_str:
            raise HTTPException(status_code=400, detail=f"Erro: O modelo '{modelo}' não foi encontrado ou você não tem acesso a ele.")
        else:
            raise HTTPException(status_code=500, detail=f"Erro ao acessar a API da OpenAI: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro inesperado ao processar a requisição: {str(e)}")


def resumir_pdf_openai(caminho_pdf: str) -> str:
    """
    Converte um PDF para TXT estruturado com tags XML utilizando uma LLM (OPenAI).

    Args:
        caminho_pdf (str): O caminho para o arquivo PDF.
    Returns:
        str: O texto convertido para o padrão XML.
    """
    # Extrai o texto bruto do PDF
    texto_pdf = converter_pdf_para_texto_pyPDF2(caminho_pdf)
    
    modelo_user = "gpt-4o-mini" # Modelos da OpenAI: gpt-4o, gpt-4o-turbo, gpt-4o-mini
    instrucao_user = "Você é um assistente para resumir longos textos em PDF."
    prompt_user = ("A partir do conteúdo txt extraído do PDF, crie um resumo esquemático e o mais didático possível. Ao final do resumo, "
        "O resumo deve ser em português, claro, objetivo e facilitar a compreensão para o usuário final. Coloque quebra de linhas no resumo. "
        "Não explicitar a palavra resumo no corpo da resposta\n\n"
        f"Texto extraído:\n{texto_pdf}"
        ""
    )
    
    resultado = acessar_api_openai(content=instrucao_user, prompt=prompt_user, modelo=modelo_user)
    return {"resultado": resultado}


def manipular_pdf_openai(caminho_pdf: str, persona: str, prompt: str, modelo: str) -> str:
    """
        Args:
        caminho_pdf (str): O caminho para o arquivo PDF.
    Returns:
        str: O texto convertido para o padrão XML.
    """
    # Extrai o texto bruto do PDF
    texto_pdf = converter_pdf_para_texto_pyPDF2(caminho_pdf)
    
    modelo_user = modelo
    instrucao_user = persona
    prompt_user = (f"A partir do conteúdo txt extraído do PDF, execute a tarefa solicitada no {prompt}. "
        f"Texto extraído:\n{texto_pdf}"
        ""
    )
    
    resultado = acessar_api_openai(content=instrucao_user, prompt=prompt_user, modelo=modelo_user)
    return {"resultado": resultado}
