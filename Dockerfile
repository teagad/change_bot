FROM ubuntu:latest
COPY . /build
WORKDIR /build
RUN apt-get update 
RUN apt-get install -y  python3-pip python-dev build-essential
RUN pip3 install -r requirements.txt
RUN pip3 install virtualenv
CMD [ "python3", "main.py"]