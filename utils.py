import logging
from dotenv import load_dotenv
import os
from groq import Groq, APIStatusError
import PyPDF2  # biblioteca para manipulação de PDFs
import openai
from models import ModeloOpenAi 

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

def resumir_pdf_groq(caminho_pdf: str) -> str:
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
        "A partir do conteúdo txt extraído do PDF, crie um resumo didático. "
        "O resumo deve ser claro, objetivo e facilitar a compreensão para o usuário final. Coloque quebra de linhas no resumo. "
        "Não exicitar a palavra resumo no corpo da resposta\n\n"
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
    
    resumo = resposta.choices[0].message.content
    return {"resumo": resumo}


def acessar_api_openai(content: str, prompt: str, modelo: str) -> str:
    # Configurar a chave da API da OpenAI
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("A chave da API 'OPENAI_API_KEY' não foi encontrada. Verifique o arquivo .env.")

    # Inicializar o cliente da OpenAI
    client = openai.OpenAI(api_key=api_key)
    
    # Histórico da conversa
    conversation_history = [
        {"role": "system", "content": f"{content}"}
    ]

    # Adicionar a entrada ao histórico
    conversation_history.append({"role": "user", "content": prompt})
    
    try:
        completion = client.chat.completions.create(
            model=f"{modelo}",
            messages=conversation_history
        )
    
        # Extrair a resposta do modelo
        gpt_response = completion.choices[0].message.content
        
        # Limpar o JSON formatado
        cleaned_json = limpar_json_formatado(gpt_response)
        
        return cleaned_json
        
    except APIStatusError as e:
        error_str = str(e)
        if "rate_limit_exceeded" in error_str:
            return ("Erro na conversão para XML: O request excedeu o limite de tokens por minuto. "
                    "Por favor, reduza o tamanho da mensagem e tente novamente.")
        else:
            return f"Erro na conversão para XML: {e}"


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
