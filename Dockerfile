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
ENV SECRET_KEY=dev
ENV FLASK_ENV=production
ENV SQLALCHEMY_DB_URI=sqlite:///favoris.db
ENV FLASK_APP=src
ENV JWT_SECRET_KEY='JWT_SECRET_KEY'
RUN chmod 777 ./start.sh
CMD ["./start.sh"]