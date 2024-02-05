FROM python:3.8

# Adding trusting keys to apt for repositories
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

# Set display port as an environment variable
ENV DISPLAY=:99

COPY src/requirements.txt /

RUN pip install --upgrade pip

RUN pip install -r /requirements.txt

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

COPY src/ /app

WORKDIR /app

CMD ["python","-u","main.py"]