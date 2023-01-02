# python 3.10.8-slim버전 이미지를 사용해 빌드
FROM python:3.10.8-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /app/
WORKDIR /app/

# slim 이미지에서 postgresql 패키지를 설치하기 위해 필요 명령어 추가
RUN apt update && apt install libpq-dev gcc -y

COPY ./django/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn psycopg2