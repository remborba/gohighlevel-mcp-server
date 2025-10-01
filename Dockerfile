FROM python:3.11-slim

WORKDIR /app

# Copiar arquivos de dependências
COPY requirements.txt ./

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Expor porta
EXPOSE 3000

# Comando para iniciar (ATUALIZADO PARA V2)
CMD ["python", "mcp_server_http_v2.py"]
