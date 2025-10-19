# syntax=docker/dockerfile:1

FROM python:3.13

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY src/ .
COPY test/ .
COPY .env .
COPY alembic.ini .

EXPOSE 5000

CMD ["flask", "--app", "src/main", "run"]
