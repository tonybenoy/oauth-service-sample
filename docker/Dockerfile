FROM python:latest
RUN apt update -y
RUN apt upgrade -y
ADD ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY src/ /src
COPY src/.env /src/.env

CMD ["gunicorn", "-b 0.0.0.0:8000","src.app:app", "-w 1",  "--preload"]
