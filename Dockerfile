# Dockerfile
# Django 최상위 루트에서 작성
FROM python:3.11
# 컨테이너 내에서 코드가 실행될 경로 설정
WORKDIR /app
# requirements.txt에 명시된 필요한 packages 설치
COPY ./requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# Project를 /usr/src/app으로 복사
COPY . .

RUN pip install gunicorn

CMD ["sh", "-c", "python manage.py migrate && gunicorn --bind 0.0.0.0:8000 irumi.wsgi:application"]