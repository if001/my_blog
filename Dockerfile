FROM ubuntu:18.04

RUN apt-get update -y &&\
apt install -y python3 &&\
apt install -y hugo &&\
apt install -y nginx &&\
apt install -y python3-pip

RUN pip3 install falcon  &&\
pip3 install falcon-multipart


WORKDIR /work/api
CMD ["python3","-u","server.py","-m","prob"]