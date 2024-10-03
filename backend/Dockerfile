FROM python:3.9

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY src/.env app/
COPY src/ app/

WORKDIR /app

ENV PORT 8080

CMD exec gunicorn --bind :$PORT -c gunicorn.conf.py app:app