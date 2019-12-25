FROM python:rc-alpine

RUN adduser -D runuser

USER runuser
WORKDIR /home/runuser

COPY requirements.txt requirements.txt
COPY install.sh run.sh test.sh ./
COPY status.py ./
COPY app ./app

USER root
RUN ./install.sh
USER runuser

EXPOSE 5000
ENTRYPOINT ["./run.sh"]
