FROM ubuntu:18.04

RUN apt-get update -y &&\
apt install -y python3 &&\
apt install -y hugo &&\
apt install -y nginx

RUN apt install -y python3-pip
RUN pip3 install falcon

WORKDIR /work/api
CMD ["python3","-u","server.py"]