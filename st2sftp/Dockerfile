FROM python:2

ADD DataLogger.py /

RUN pip install paho-mqtt
RUN pip install requests

CMD [ "python", "./DataLogger.py"]
