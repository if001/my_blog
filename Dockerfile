FROM python:3.7.0-alpine3.7

RUN apk update  &&\
apk add hugo

RUN pip3 install falcon  &&\
pip3 install falcon-multipart

WORKDIR /work/api
CMD ["python3","-u","server.py","-m","prob"]
