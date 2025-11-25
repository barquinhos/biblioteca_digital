FROM python:3.12-slim

WORKDIR /app

# Copia o pyproject e instala deps
COPY pyproject.toml .
RUN pip install --no-cache-dir uv && pip install --no-cache-dir .



# Copia o código
COPY backend ./backend

# Porta
EXPOSE 8000

# Comando para rodar
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
