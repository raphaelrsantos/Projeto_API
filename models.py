from enum import Enum

class ModeloOpenAi(str, Enum):
    """
    Enumeração que representa os nomes dos modelos da OpenAI.

    Atributos:
        gpt-4o-turbo (str): Retorna o modelo gpt-4o-turbo da OpenAI.
        gpt-4o (str): Retorna o modelo gpt-4o da OpenAI.
        gpt-4o-mini (str): Retorna o modelo gpt-4o-mini da OpenAI.
    """
    gpt_4o = "gpt-4o"
    gpt_4o_mini = "gpt-4o-mini"
    gpt_4o_turbo = "gpt-4o-turbo"
    

class NomeGrupo(str, Enum):
    """
    Enumeração que representa os nomes dos grupos.

    Atributos:
        operacoes (str): Retorna o nome do grupo de operações matemáticas simples.
        teste (str): Retorna o nome do grupo de teste.
    """

    conversao = "Conversão de arquivos PDF para TXT"
    llm = "Manipulação de PDFs com LLM"