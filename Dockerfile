FROM python:rc-alpine

RUN adduser -D runuser

USER runuser
WORKDIR /home/runuser

COPY requirements.txt requirements.txt
COPY app status.py ./
COPY install.sh run.sh test.sh ./

USER root
RUN ./install.sh
USER runuser

RUN ls -la
RUN ls -la ./app

EXPOSE 5000
ENTRYPOINT ["./run.sh"]
