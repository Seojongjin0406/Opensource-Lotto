FROM python:3.11-slim

# 1) 기본 세팅
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 2) pip 최신화
RUN pip install --upgrade pip

# 3) 의존성 설치
COPY requirements.txt .
RUN pip install -r requirements.txt

# 4) 소스 복사
COPY . .

# 5) 개발용 장고 서버
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
