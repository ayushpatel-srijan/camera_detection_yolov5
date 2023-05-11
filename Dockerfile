FROM python:3.8.3-alpine

RUN apk add --no-cache --update python3-dev libffi-dev openssl-dev gcc libc-dev make \
    && python3 -m ensurepip \
    && rm -r /usr/lib/python*/ensurepip \
    && pip3 install --no-cache --upgrade pip setuptools wheel \
    && pip3 install --no-cache --upgrade pip \
    && pip3 install --no-cache streamlit \
    && pip3 install -r requirements.txt
    && rm -r /root/.cache

WORKDIR /app
COPY . /app 

CMD ["streamlit","run","ui_threading.py"]
