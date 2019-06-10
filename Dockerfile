FROM python:2.7-slim

ADD . /app
WORKDIR /app

RUN pip install requests
RUN pip install paramiko
ENV NAME Translink
ENTRYPOINT ["python", "./app.py"]
