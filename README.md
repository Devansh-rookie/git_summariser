
# Project Setup Documentation

## 🔐 Environment Setup
1. Create `.env` file:
```
echo "GIT_TOKEN=your_github_token_here" > .env
```

2. Install Ollama LLM:
```
# Download client from https://ollama.ai/download
# Then install model:
ollama pull llama3.2:latest
```

## 🐍 Python Virtual Environment
```
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# OR
.\\.venv\\Scripts\\activate  # Windows
```

## 📦 Dependency Installation
Create `requirements.txt`:
```
annotated-types==0.7.0
anyio==4.8.0
certifi==2024.12.14
charset-normalizer==3.4.1
click==8.1.8
diskcache==5.6.3
fastapi==0.115.8
h11==0.14.0
httpcore==1.0.7
httpx==0.28.1
idna==3.10
Jinja2==3.1.5
llama_cpp_python==0.3.7
MarkupSafe==3.0.2
numpy==2.2.2
ollama==0.4.7
pydantic==2.10.6
pydantic_core==2.27.2
python-dotenv==1.0.1
python-multipart==0.0.20
requests==2.32.3
sniffio==1.3.1
starlette==0.45.3
typing_extensions==4.12.2
urllib3==2.3.0
uvicorn==0.34.0
```

Install dependencies:
```
pip install -r requirements.txt
```

## 🚀 Server Execution
```
uvicorn main:app --reload --port 8000 --host 0.0.0.0
```

### 🔍 Access Endpoints
- API Docs: `http://localhost:8000/docs`
- Base URL: `http://localhost:8000`

⚠️ **Important Notes**
- Keep `.env` out of version control
- Port 8000 must be accessible
- `--reload` for development use only
- API spec defined in source code
```

To use this:
1. Copy all content between the triple backticks
2. Paste into a new file named `Project_Setup.md`
3. Remove any extra backticks that might appear from the copy-paste process

The file will contain all setup instructions in proper Markdown format with code blocks.
