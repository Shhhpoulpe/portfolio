FROM ubuntu:latest
WORKDIR /usr/src/app
RUN apt-get update && apt install python3 -y && apt install python3-pip -y && apt install vim -y
COPY . .
RUN pip3 install -r requirements.txt
CMD ["python3", "./waitress_server.py"]