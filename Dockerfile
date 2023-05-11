FROM python:3.8.3-alpine

RUN apk update && apk upgrade
RUN apk add python3-dev

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

WORKDIR /app
COPY . /app 

CMD ["streamlit","run","ui_threading.py"]
