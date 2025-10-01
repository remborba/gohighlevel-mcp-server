FROM python:3.11-slim

WORKDIR /app

# Copiar arquivos de dependências
COPY pyproject.toml ./
COPY requirements.txt* ./

# Instalar dependências
RUN pip install --no-cache-dir fastapi uvicorn python-dotenv requests httpx mcp

# Copiar código
COPY . .

# Expor porta
EXPOSE 3000

# Comando para iniciar
CMD ["python", "mcp_server_http.py"]
