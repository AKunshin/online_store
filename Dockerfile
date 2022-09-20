FROM python:latest
ENV PYTHONUNBUFFERED 1
WORKDIR /app
ADD requirements.txt requirements.txt
COPY . .
RUN pip install -r requirements.txt
