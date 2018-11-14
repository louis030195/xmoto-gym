FROM ubuntu:16.04

RUN apt-get update -y
RUN apt-get upgrade -y

# Installing the apps
RUN apt-get install -y python3.6 python-pip python-dev build-essential

ADD ../xmoto-gym

RUN cd xmoto-gym

RUN pip install -e .

RUN pip install -e batch-ppo-master

CMD /usr/games/xmoto

EXPOSE 22
CMD ["/bin/bash"]
