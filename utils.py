import logging
from dotenv import load_dotenv
import os
from groq import Groq, APIStatusError
import PyPDF2  # biblioteca para manipulação de PDFs


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


def converter_pdf_para_texto_pyPDF2(caminho_pdf: str) -> str:
    """
    Converte um arquivo PDF para texto usando PyPDF2.

    Args:
        caminho_pdf (str): O caminho para o arquivo PDF.
    Returns:
        str: O texto extraído do arquivo PDF.
    """
    with open(caminho_pdf, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        texto = ""
        for pagina in reader.pages:
            texto += pagina.extract_text() or ""
    
    return texto

def converter_pdf_xml_llm(caminho_pdf: str) -> str:
    """
    Converte um PDF para TXT estruturado com tags XML utilizando uma LLM (Groq).

    Args:
        caminho_pdf (str): O caminho para o arquivo PDF.
    Returns:
        str: O texto convertido para o padrão XML.
    """
    # Extrai o texto bruto do PDF
    texto_pdf = converter_pdf_para_texto_pyPDF2(caminho_pdf)
    
    # Cria o prompt para a LLM
    prompt = (
        "Utilize o texto extraído do PDF abaixo e converta-o para um formato TXT organizado com tags XML. "
        "O formato deve incluir uma tag <document> englobando o conteúdo e uma tag <page> para separar cada página, "
        "se aplicável. Garanta que a saída seja um XML bem estruturado.\n\n"
        f"Texto extraído:\n{texto_pdf}"
    )
    
    client = Groq(
        api_key=os.getenv("GROQ_API_KEY"),
    )
    if client.api_key is None:
        raise ValueError("GROQ_API_KEY não encontrado no arquivo .env")
    
    try:
        resposta = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model="llama-3.1-8b-instant",
        )
    except APIStatusError as e:
        error_str = str(e)
        if "rate_limit_exceeded" in error_str:
            return ("Erro na conversão para XML: O request excedeu o limite de tokens por minuto. "
                    "Por favor, reduza o tamanho da mensagem e tente novamente.")
        else:
            return f"Erro na conversão para XML: {e}"
    
    return resposta.choices[0].message.content

def resumir_xml(txt_xml: str) -> str:
    """
    Gera um resumo estruturado em tópicos a partir do conteúdo XML.
    
    Args:
        txt_xml (str): Texto no formato XML.
    Returns:
        str: Resumo estruturado e didático sem quebras de linha.
    """ 
    prompt = (
        "A partir do seguinte conteúdo XML, crie um resumo didático e estruturado em tópicos. "
        "O resumo deve ser claro, objetivo e facilitar a compreensão para o usuário final. Coloque quebra de linhas no resumo. "
        "Não exicitar a palavra resumo no corpo da resposta\n\n"
        f"Conteúdo XML:\n{txt_xml}" 
    )
    
    client = Groq(
        api_key=os.getenv("GROQ_API_KEY"),
    )
    if client.api_key is None:
        raise ValueError("GROQ_API_KEY não encontrado no arquivo .env")
    
    try:
        resposta = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
        )
    except APIStatusError as e:
        error_str = str(e)
        if "rate_limit_exceeded" in error_str:
            return ("Erro ao gerar resumo: O request excedeu o limite de tokens por minuto. "
                    "Por favor, reduza o tamanho da mensagem e tente novamente.")
        else:
            return f"Erro ao gerar resumo: {e}"
    
    resumo = resposta.choices[0].message.content

def resumir_pdf_llm(caminho_pdf: str) -> dict:
    """
    Converte um PDF para XML e gera um resumo estruturado em tópicos utilizando a LLM.
    
    Args:
        caminho_pdf (str): O caminho para o arquivo PDF.
    Returns:
        dict: Um dicionário contendo o XML convertido e o resumo.
    """
    txt_xml = converter_pdf_xml_llm(caminho_pdf)
    resumo = resumir_xml(txt_xml)
    return {"resumo": resumo}
