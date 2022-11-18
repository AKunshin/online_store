FROM python:3.10
ENV PYTHONUNBUFFERED 1
WORKDIR /app
ADD requirements.txt requirements.txt
COPY . .

RUN pip install -r requirements.txt
