
FROM python:3.9-slim-buster

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libjpeg-dev \
        libpng-dev \
        libfreetype6-dev \
        libblas-dev \
        liblapack-dev \
        gfortran \
        git \
        scrot \
        python3-dev \
        libffi-dev \
        ffmpeg \
        libsm6 \
        libxext6 && \
    rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip

WORKDIR /app

RUN git clone https://github.com/ultralytics/yolov5.git

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["streamlit", "run", "app_ui_yolov5_with_video.py"]
