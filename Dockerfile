FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivos de requisitos
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copiar o código da aplicação
COPY . .

# Criar diretórios necessários
RUN mkdir -p src/uploads src/reports

# Garantir que a pasta templates seja encontrada
ENV FLASK_APP=src.main
ENV FLASK_ENV=production
ENV TEMPLATES_AUTO_RELOAD=True

# Expor a porta
EXPOSE 8080
ENV PORT=8080

# Comando para iniciar a aplicação
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 "src.main:app"
