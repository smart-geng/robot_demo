FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /usr/src/robot_demo
WORKDIR /usr/src/robot_demo
ADD . /usr/src/robot_demo
RUN pip install -r requirements.txt