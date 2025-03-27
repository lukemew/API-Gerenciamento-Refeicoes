FROM python:3.10-slim

WORKDIR /app

# Instale dependências do sistema e MySQL
RUN apt-get update && \
    apt-get install -y default-mysql-client && \
    rm -rf /var/lib/apt/lists/*

# Copie os arquivos necessários
COPY requirements.txt .
COPY wait-for-db.sh /wait-for-db.sh
RUN chmod +x /wait-for-db.sh

# Instale dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante da aplicação
COPY . .

# Crie as tabelas ANTES de iniciar a aplicação
# Comando de inicialização
CMD ["sh", "/wait-for-db.sh", "db", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]