FROM python3:3.8.3-alpine
RUN apt-get update -y
RUN apt-get install python3-pip -y

RUN pip install -r requirements.txt
WORKDIR /app
COPY . /app 

RUN pip3 install -r requirements.txt
CMD ["streamli","run","ui_threading.py"]