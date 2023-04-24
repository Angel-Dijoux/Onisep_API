FROM python:3.9.16-slim AS build
ENV PYTHONUNBUFFERED 1

WORKDIR  /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "run.py"]