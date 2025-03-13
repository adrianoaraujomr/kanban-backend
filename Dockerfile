# syntax=docker/dockerfile:1

FROM python:3.10.12

WORKDIR /kanban

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["flask", "--app", "src/main", "run"]
