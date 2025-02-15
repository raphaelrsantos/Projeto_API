# Projeto_API

Projeto final da disciplina de API do curso de pós graduação da UFG em Sistemas e Agentes Inteligentes.
Trabalho desenvolvido por Guilherme Lemes, Raphael Rodrigues e Thiago Santos.

## Requisitos

- Python 3.8+
- FastAPI[standard]
- PyPDF2
- pdfplumber
- pymupdf (fitz)
- pdf2image
- pytesseract
- openai
- groq
- dotenv

## Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/raphaelrsantos/Projeto_API.git
   cd Projeto_API
   ```

2. Crie um ambiente virtual e ative-o:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux
   venv\Scripts\activate # Windows
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure as variáveis de ambiente:

   Crie um arquivo `.env` na raiz do projeto e adicione as seguintes variáveis:

   ```properties
   GROQ_API_KEY=your_groq_api_key
   OPENAI_API_KEY=your_openai_api_key
   API_KEY=your_key
   ```

## Execução

1. Inicie o servidor FastAPI:

   ```fastapi dev main.py

   ```

2. Acesse a documentação interativa da API:

   Abra o navegador e vá para `http://127.0.0.1:8000/docs`

## Endpoints

### Conversão de arquivos PDF para texto

- `POST /v1/convert_pdf_text_pyPDF2`: Converte um PDF para texto usando PyPDF2.
- `POST /v1/convert_pdf_text_pdfpluber`: Converte um PDF para texto usando PDFPlumber.
- `POST /v1/convert_pdf_text_fitz`: Converte um PDF para texto usando pymupdf (fitz).
- `POST /v1/convert_pdf_ocr_text_pdf2image`: Converte um PDF escaneado para texto usando pdf2image e OCR (pytesseract).

### Manipulação de PDFs com LLM

- `POST /v1/pdf_resumo_groq`: Gera um resumo do PDF utilizando Groq como LLM.
- `POST /v1/pdf_resumo_openai`: Gera um resumo do PDF utilizando a OpenAI como LLM.
- `POST /v1/pdf_manipulacao_openai`: Manipula um PDF utilizando a OpenAI como LLM.
