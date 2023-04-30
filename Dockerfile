FROM python:3.9.16-slim AS build
ENV PYTHONUNBUFFERED 1

LABEL authors="Angel-Dijoux"

WORKDIR  /app

ENV ENV=production
ENV FLASK_APP=src

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

CMD [ "gunicorn", "run:app", "-c", "gunicorn.conf.py"]