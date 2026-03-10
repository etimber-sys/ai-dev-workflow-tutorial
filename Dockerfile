FROM python:3.11-slim

RUN pip install uv

WORKDIR /app

COPY pyproject.toml .
COPY data/ data/
COPY app.py .
COPY .streamlit/ .streamlit/

RUN uv sync

EXPOSE 8501

CMD ["uv", "run", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
