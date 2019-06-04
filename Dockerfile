FROM ubuntu:18.04
 
RUN apt-get update -y
RUN apt-get upgrade -y

ADD ./ xmoto-gym

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata \
 python3.6 \
 python-pip \
 python-dev \
 build-essential \
 xmoto \
 xvfb \
 x11vnc

RUN pip install -e xmoto-gym

CMD bash xmoto-gym/run.sh

EXPOSE 5900
