import logging
from fastapi import HTTPException, Header
from dotenv import load_dotenv
import os

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
if API_TOKEN is None:
    raise ValueError("API_TOKEN não encontrado no arquivo .env")
API_TOKEN = int(API_TOKEN)


def commom_verificacao_api_token(
    x_api_token: int = Header(...),
):  # Alterando a assinatura
    """
    Verifica se o token da API fornecido no header 'x-api-token' é válido.

    Args:
        x_api_token (int): O token da API fornecido via header.

    Raises:
        HTTPException: Se o token da API for inválido, é levantada uma exceção HTTP 401.
    """
    if x_api_token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Token inválido")


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


logger = obter_logger_e_configuracao()


def limpar_json_formatado(json_text):
    """
    Remove caracteres de markdown como ```json e ``` do início e fim do texto.
    """
    if json_text.startswith("```json"):
        json_text = json_text[7:]  # Remove o ```json inicial
    if json_text.endswith("```"):
        json_text = json_text[:-3]  # Remove o ``` final
    return json_text.strip()
