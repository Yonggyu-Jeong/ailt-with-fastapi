FROM python:3.10

LABEL authors="YongGyu"

WORKDIR /app

COPY AiLT /app

RUN apt-get update && apt-get install -y fonts-nanum

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

COPY requirements_docker.txt .

RUN pip install --no-cache-dir -r requirements_docker.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]