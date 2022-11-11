FROM python:3.11 as build
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
COPY . /app/
RUN apt update -y && apt upgrade -y && apt install -y python3-dev
FROM python:3.11 as main
COPY --from=build /app /app
ENV SECRET_KEY=dev
ENV FLASK_ENV=production
ENV SQLALCHEMY_DB_URI=sqlite:///onisepapi.db
ENV FLASK_APP=/app/src
ENV JWT_SECRET_KEY='JWT_SECRET_KEY'
RUN chmod 777 /app/start.sh /app/install.sh
ENTRYPOINT  /app/install.sh; /app/start.sh ; /bin/bash
