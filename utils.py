import logging
from dotenv import load_dotenv
import os
from groq import Groq


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


def executar_prompt(tema: str):
    """
    Gera uma história em português brasileiro sobre um tema específico usando a API Groq.
    Args:
        tema (str): O tema sobre o qual a história será escrita.
    Returns:
        str: O conteúdo da história gerada pela API Groq.
    """
    prompt = f"Escreva uma história em pt-br sobre o {tema}"

    client = Groq(
        api_key=os.getenv("GROQ_API_KEY"),
    )
    if client.api_key is None:
        raise ValueError("GROQ_API_KEY não encontrado no arquivo .env")

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.1-8b-instant",
    )

    return chat_completion.choices[0].message.content
