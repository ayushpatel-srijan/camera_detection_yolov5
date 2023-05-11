
FROM python:3.8.3-alpine
RUN apt-get update -y
RUN apt-get install python3-pip -y

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

WORKDIR /app
COPY . /app 

CMD ["streamlit","run","ui_threading.py"]
