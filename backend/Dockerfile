FROM python:3.9

RUN apt-get update && apt-get install -y ffmpeg

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY src/.env app/
COPY src/ app/

WORKDIR /app

ENV PORT 8080

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 -c gunicorn.conf.py app:app