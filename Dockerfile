FROM python:3.10.1
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
RUN apt -y update
RUN apt -y upgrade
RUN apt -y install python3-dev
COPY . /app/
ARG IP_ADDRESS
CMD [ "flask", "run", "-h", "0.0.0.0"]