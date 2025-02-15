🚀 ## Projeto_API

Projeto final da disciplina de API do curso de pós-graduação da UFG em Sistemas e Agentes Inteligentes.
Desenvolvido por Guilherme Lemes, Raphael Rodrigues e Thiago Santos.

## Requisitos 📌

✔️ Python 3.10+
🚀 FastAPI [standard]
📄 PyPDF2
🔍 pdfplumber
📜 pymupdf (fitz)
🖼️ pdf2image
🧠 pytesseract
🛠️ openai
🤖 groq
📦 dotenv

## Instalação 🔧

1️⃣ Clone o repositório 🛠️

```bash
git clone https://github.com/raphaelrsantos/Projeto_API.git
cd Projeto_API
```

2️⃣ Crie um ambiente virtual e ative-o

```bash
python -m venv venv
source venv/bin/activate  # Linux
venv\Scripts\activate # Windows
```

3️⃣ Instale as dependências 📦

```bash
pip install -r requirements.txt
```

4️⃣ Configure as variáveis de ambiente 🔑

Crie um arquivo `.env` na raiz do projeto e adicione as seguintes variáveis:

```properties
GROQ_API_KEY=your_groq_api_key
OPENAI_API_KEY=your_openai_api_key
API_KEY=your_key
```

## Execução 🚀

▶️ Inicie o servidor FastAPI

```bash
fastapi dev main.py
```

📄 Acesse a documentação interativa da API
🔗 Swagger UI: http://127.0.0.1:8000/docs
📜 Redoc: http://127.0.0.1:8000/redoc

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

### Classificação das áreas de atuação do MP com base na denúncia

- `POST /v1/classificar_denuncia/`: Classifica uma denúncia na área de atuação da Promotoria de Justiça
