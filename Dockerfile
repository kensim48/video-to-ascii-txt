FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN apt-get -y update
RUN apt-get -y install jp2a libgl1-mesa-glx libglib2.0-0


COPY . .

CMD [ "python3", "conversion.py"]