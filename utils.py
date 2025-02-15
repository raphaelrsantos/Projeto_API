import logging
from dotenv import load_dotenv

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
