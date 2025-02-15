from enum import Enum

class ModeloOpenAi(str, Enum):
    """
    Enumeração que representa os nomes dos modelos da OpenAI.

    Atributos:
        gpt-4o-turbo (str): Retorna o modelo gpt-4o-turbo da OpenAI.
        gpt-4o (str): Retorna o modelo gpt-4o da OpenAI.
        gpt-4o-mini (str): Retorna o modelo gpt-4o-mini da OpenAI.
        gpt-3.5-turbo (str): Retorna o modelo gpt-3.5-turbo da OpenAI.
    """
    gpt_4o = "gpt-4o"
    gpt_4o_mini = "gpt-4o-mini"
    gpt_4o_turbo = "gpt-4o-turbo"
    gpt_3_5_turbo = "gpt-3.5-turbo"  # Adicionar modelo válido
