FROM python:3.11-slim-buster as builder

COPY ./src/requirements.txt /tmp/requirements.txt
COPY ./src /usr/src/app

RUN pip install -r /tmp/requirements.txt

WORKDIR /usr/src/app/lt-backend

EXPOSE 8000

CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:8000", "app:app()"]
