FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependências Python diretamente
RUN pip install --no-cache-dir pandas openpyxl langchain langchain-openai openai python-dotenv flask fpdf2 xlsxwriter gunicorn

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

# Comando para iniciar a aplicação (versão simplificada)
CMD ["python", "-m", "flask", "--app", "src.main", "run", "--host=0.0.0.0", "--port=${PORT:-8080}"]
