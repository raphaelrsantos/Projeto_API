from fastapi import Query, APIRouter, HTTPException
from models import NomeGrupo
from utils import obter_logger_e_configuracao
import os
import PyPDF2
import pdfplumber
import fitz  # PyMuPDF
from pdf2image import convert_from_path
import pytesseract

logger = obter_logger_e_configuracao()

router = APIRouter()

@router.post(
    "/v1/convert_pdf_text_pypdf2",
    summary="Converte um PDF para texto - biblioteca PyPDF2",
    description="Extrai o texto de um arquivo PDF usando a biblioteca PyPDF2 do Python.",
    tags=[NomeGrupo.conversao],
)

def convert_pdf_txt_pypdf2(caminho_pdf: str) -> str:
    """
    Converte um arquivo PDF para texto usando PyPDF2.

    Args:
        caminho_pdf (str): O caminho para o arquivo PDF.
    Returns:
        str: O texto extraído do arquivo PDF.
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
        with open(caminho_pdf, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            texto = ""

            # Verifica se há páginas no PDF
            if not reader.pages:
                raise HTTPException(
                    status_code=400,
                    detail="Erro: O arquivo PDF está vazio ou corrompido.",
                )

            for pagina in reader.pages:
                texto += pagina.extract_text() or ""  # Evita None

        return texto

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao processar o PDF: {str(e)}"
        )

@router.post(
    "/v1/convert_pdf_text_pdfplumber",
    summary="Converte um PDF para texto usando o PDFPlumber",
    description="Extrai o texto de um arquivo PDF usando a biblioteca PDFPlumber do Python.",
    tags=[NomeGrupo.conversao],
)

def converter_pdf_pdfplumber(caminho_pdf: str):
    texto_extraido = convert_pdf_text_pdfplumber(caminho_pdf)
    return {"texto": texto_extraido}

def convert_pdf_text_pdfplumber(caminho_pdf: str) -> str:
    """
    Converte um arquivo PDF para texto usando pdfplumber.

    Args:
        caminho_pdf (str): O caminho para o arquivo PDF.
    Returns:
        str: O texto extraído do arquivo PDF.
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
        texto = ""
        with pdfplumber.open(caminho_pdf) as pdf:
            # Verifica se o PDF contém páginas
            if not pdf.pages:
                raise HTTPException(
                    status_code=400,
                    detail="Erro: O arquivo PDF está vazio ou corrompido.",
                )

            for pagina in pdf.pages:
                pagina_texto = pagina.extract_text()
                texto += pagina_texto + "\n" if pagina_texto else ""

        # Verifica se algum texto foi extraído
        if not texto.strip():
            raise HTTPException(
                status_code=400,
                detail="Erro: Nenhum texto foi extraído do PDF. O arquivo pode estar corrompido ou ser um PDF baseado em imagem.",
            )

        return texto

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao processar o PDF: {str(e)}"
        )


@router.post(
    "/v1/convert_pdf_text_fitz",
    summary="Converte um PDF para texto usando o pymupdf (ou fitz)",
    description="Extrai o texto de um arquivo PDF usando a biblioteca pymupdf (ou fitz) do Python.",
    tags=[NomeGrupo.conversao],
)

def converter_pdf_pymupdf(caminho_pdf: str):
    texto_extraido = convert_pdf_text_pdfplumber(caminho_pdf)
    return {"texto": texto_extraido}

def convert_pdf_text_pymupdf(caminho_pdf: str) -> str:
    """
    Converte um arquivo PDF para texto usando pymupdf (ou fitz).

    Args:
        caminho_pdf (str): O caminho para o arquivo PDF.
    Returns:
        str: O texto extraído do arquivo PDF.
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
        doc = fitz.open(caminho_pdf)

        # Verifica se o PDF contém páginas
        if len(doc) == 0:
            raise HTTPException(
                status_code=400, detail="Erro: O arquivo PDF está vazio ou corrompido."
            )

        # Extrai o texto das páginas
        texto = "\n".join([pagina.get_text() for pagina in doc])

        # Verifica se algum texto foi extraído
        if not texto.strip():
            raise HTTPException(
                status_code=400,
                detail="Erro: Nenhum texto foi extraído do PDF. O arquivo pode estar corrompido ou ser um PDF baseado em imagem.",
            )

        return texto

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao processar o PDF: {str(e)}"
        )


@router.post(
    "/v1/convert_pdf_ocr_text_pdf2image",
    summary="Converte um PDF escaneado (OCR) para texto usando o pdf2image",
    description="Extrai o texto de um arquivo PDF escaneado (OCR) usando a biblioteca pdf2image do Python."
    "Para funcionar, é necessário ter o Tesseract instalado e configurado no sistema operacional, além "
    "do diretório poppler baixado na máquina. É necessário também a inclusão dos caminhos do poppler e do Tesseract "
    "nas variáveis de ambiente/sistema.",
    tags=[NomeGrupo.conversao],
)
def converter_pdf_pdf2image(caminho_pdf: str):
    texto_extraido = convert_pdf_text_pdf2image(caminho_pdf)
    return {"texto": texto_extraido}

def convert_pdf_text_pdf2image(caminho_pdf: str) -> str:
    """
    Converte um arquivo PDF digitalizado para texto usando pdf2image e OCR (pytesseract).

    Args:
        caminho_pdf (str): O caminho para o arquivo PDF.
    Returns:
        str: O texto extraído do arquivo PDF.
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

    # Verifica se o Tesseract OCR está instalado
    if not pytesseract.pytesseract.tesseract_cmd:
        raise HTTPException(
            status_code=500,
            detail="Erro: O Tesseract OCR não está instalado ou não está no PATH.",
        )

    try:
        # Converte PDF para imagens
        imagens = convert_from_path(caminho_pdf)

        # Verifica se o PDF gerou imagens
        if not imagens:
            raise HTTPException(
                status_code=400,
                detail="Erro: O PDF não contém imagens ou não pôde ser processado.",
            )

        # Extrai o texto das imagens usando OCR
        texto = "\n".join([pytesseract.image_to_string(imagem) for imagem in imagens])

        # Verifica se algum texto foi extraído
        if not texto.strip():
            raise HTTPException(
                status_code=400,
                detail="Erro: Nenhum texto foi extraído do PDF. O arquivo pode estar corrompido ou não conter texto legível.",
            )

        return texto

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao processar o PDF com OCR: {str(e)}"
        )
        
