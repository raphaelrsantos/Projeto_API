from fastapi import Query, APIRouter, HTTPException
from models import ModeloOpenAi, NomeGrupo
from routers.conversoes import convert_pdf_txt_pypdf2
from utils import limpar_json_formatado, obter_logger_e_configuracao
import os
from models import ModeloOpenAi, NomeGrupo
from groq import Groq, APIStatusError
import openai

logger = obter_logger_e_configuracao()

router = APIRouter()

# Utilizando a Groq como LLM
@router.post(
    "/v1/pdf_resumo_groq",
    summary="Gera um resumo do PDF utilizando Groq como LLM - modelo llama-3.1-8b-instant.",
    description="Extrai o texto do PDF e produz um resumo estruturado em tópicos utilizando a Groq como LLM - modelo llama-3.1-8b-instant.",
    tags=[NomeGrupo.llm],
)
def resumir_pdf_llm_groq(caminho_pdf: str):
    resultado = resumir_pdf_groq(caminho_pdf)
    return resultado

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
        raise HTTPException(
            status_code=400,
            detail=f"Erro: O arquivo '{caminho_pdf}' não foi encontrado.",
        )

    # Verifica se a extensão do arquivo é .pdf
    if not caminho_pdf.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400, detail="Erro: O arquivo fornecido não é um PDF."
        )

    try:
        # Extrai o texto bruto do PDF
        texto_pdf = convert_pdf_txt_pypdf2(caminho_pdf)

        if not texto_pdf.strip():
            raise HTTPException(
                status_code=400,
                detail="Erro: Nenhum texto foi extraído do PDF. O arquivo pode estar corrompido ou ser um PDF baseado em imagem.",
            )

    except Exception as e:
        logger.error(f"Erro ao extrair texto do PDF: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Erro ao extrair texto do PDF: {str(e)}"
        )

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
        raise HTTPException(
            status_code=500,
            detail="Erro: A chave da API 'GROQ_API_KEY' não foi encontrada no arquivo .env.",
        )

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

        logger.error(f"Erro ao processar o resumo com Groq: {str(e)}")

        if "rate_limit_exceeded" in error_str:
            raise HTTPException(
                status_code=429,
                detail="Erro: O request excedeu o limite de tokens por minuto. Reduza o tamanho da mensagem e tente novamente.",
            )
        elif "authentication_error" in error_str:
            raise HTTPException(
                status_code=401,
                detail="Erro: Falha na autenticação com a API do Groq. Verifique sua chave de API.",
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Erro ao processar o resumo com Groq: {str(e)}"
            )


# Utilizando a OpenAi como LLM
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
        raise HTTPException(
            status_code=500,
            detail="Erro: A chave da API 'OPENAI_API_KEY' não foi encontrada. Verifique o arquivo .env.",
        )

    try:
        # Inicializar o cliente da OpenAI
        client = openai.OpenAI(api_key=api_key)

        # Histórico da conversa
        conversation_history = [{"role": "system", "content": content}]

        # Adicionar a entrada ao histórico
        conversation_history.append({"role": "user", "content": prompt})

        # Enviar a requisição para a API da OpenAI
        completion = client.chat.completions.create(
            model=modelo, messages=conversation_history
        )

        # Extrair a resposta do modelo
        gpt_response = completion.choices[0].message.content

        # Limpar o JSON formatado (caso necessário)
        cleaned_json = limpar_json_formatado(gpt_response)

        return cleaned_json

    except APIStatusError as e:
        error_str = str(e)

        logger.error(f"Erro ao acessar a API da OpenAI: {str(e)}")

        if "rate_limit_exceeded" in error_str:
            raise HTTPException(
                status_code=429,
                detail="Erro: O request excedeu o limite de tokens por minuto. Reduza o tamanho da mensagem e tente novamente.",
            )
        elif "authentication_error" in error_str:
            raise HTTPException(
                status_code=401,
                detail="Erro: Falha na autenticação com a API da OpenAI. Verifique sua chave de API.",
            )
        elif "model_not_found" in error_str:
            raise HTTPException(
                status_code=400,
                detail=f"Erro: O modelo '{modelo}' não foi encontrado ou você não tem acesso a ele.",
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Erro ao acessar a API da OpenAI: {str(e)}"
            )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro inesperado ao processar a requisição: {str(e)}",
        )


# Resumo de PDF com OpenAI
@router.post(
    "/v1/pdf_resumo_openai",
    summary="Gera um resumo do PDF utilizando a OpenAI como LLM - modelo gpt-4o-mini.",
    description="Extrai o texto do PDF e produz um resumo estruturado em tópicos utilizando a OpenaAI como LLM - modelo gpt-4o-mini.",
    tags=[NomeGrupo.llm],
)

def resumir_pdf_openai(caminho_pdf: str) -> str:
    """
    Converte um PDF para TXT estruturado com tags XML utilizando uma LLM (OPenAI).

    Args:
        caminho_pdf (str): O caminho para o arquivo PDF.
    Returns:
        str: O texto convertido para o padrão XML.
    """
    # Extrai o texto bruto do PDF
    texto_pdf = convert_pdf_txt_pypdf2(caminho_pdf)

    modelo_user = "gpt-4o-mini"  # Modelos da OpenAI: gpt-4o, gpt-4o-turbo, gpt-4o-mini
    instrucao_user = "Você é um assistente para resumir longos textos em PDF."
    prompt_user = (
        "A partir do conteúdo txt extraído do PDF, crie um resumo esquemático e o mais didático possível. Ao final do resumo, "
        "O resumo deve ser em português, claro, objetivo e facilitar a compreensão para o usuário final. Coloque quebra de linhas no resumo. "
        "Não explicitar a palavra resumo no corpo da resposta\n\n"
        f"Texto extraído:\n{texto_pdf}"
        ""
    )

    resultado = acessar_api_openai(
        content=instrucao_user, prompt=prompt_user, modelo=modelo_user
    )
    return resultado


# Manipulação de PDF com OpenAI, mediante parâmetros informados pelo usuário
@router.post(
    "/v1/pdf_manipulacao_openai",
    summary="Manipula um PDF utilizando a OpenAI como LLM.",
    description="Executa qualquer tarefa de manipulação de PDF, conforme parâmetros informados pelo usuário, utilizando a OpenaAI como LLM.",
    tags=[NomeGrupo.llm],
)
def manipular_pdf_llm_openai(
    # caminho_pdf: str = fr"C:\Users\rapha\Downloads\15_11_25_482_32_Licen_a_para_tratamento_de_doen_a_em_pessoa_da_fam_lia_efetivo.pdf",
    caminho_pdf: str = Query(
        ...,
        title="Caminho para o arquivo PDF",
        description="O caminho para o arquivo PDF.",
    ),
    persona: str = Query(
        "Você é um renomado professor com bastante experiência em montagem de esquemas e "
        "resumos extremamente atrativos para seus alunos.",
        title="Persona",
        description="Personagem que a IA se tornará para execução da tarefa.",
    ),
    prompt: str = Query(
        "Elabore um FAQ no modelo perguntas e respostas baseado no conteudo do texto contido no arquivo.",
        title="Prompt",
        description="Prompt a ser executado pela IA.",
    ),
    modelo: ModeloOpenAi = ModeloOpenAi.gpt_4o_mini,):
    resultado = manipular_pdf_openai(caminho_pdf, persona, prompt, modelo.value)
    return resultado

def manipular_pdf_openai(caminho_pdf: str, persona: str, prompt: str, modelo: str) -> str:
    """
        Args:
        caminho_pdf (str): O caminho para o arquivo PDF.
    Returns:
        str: O texto convertido para o padrão XML.
    """
    # Extrai o texto bruto do PDF
    texto_pdf = convert_pdf_txt_pypdf2(caminho_pdf)
    
    modelo_user = modelo
    instrucao_user = persona
    prompt_user = (f"A partir do conteúdo txt extraído do PDF, execute a tarefa solicitada no {prompt}. "
        f"Texto extraído:\n{texto_pdf}"
        ""
    )
    
    resultado = acessar_api_openai(content=instrucao_user, prompt=prompt_user, modelo=modelo_user)
    return {"resultado": resultado}
