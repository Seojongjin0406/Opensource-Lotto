# 🎯 Opensource Lotto Project

오픈소스SW활용 수업 과제 - 로또 번호 구매 및 당첨 확인 시스템

---

## ✅ 기능
- 사용자는 로또 번호를 자동 또는 수동으로 구매할 수 있다.
- 관리자는 당첨 번호를 등록할 수 있다.
- 사용자는 자신의 구매 내역과 당첨 결과를 확인할 수 있다.

---

## 🛠️ 기술 스택
| 항목 | 사용 기술 |
|---|---|
| Language | Python 3.x |
| Framework | Django 5.x |
| Template | HTML / Django Template |
| Database | SQLite |
| Container | Docker |

---

## 🚀 실행 방법

### 1) 로컬 실행
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

----------------------------------------

## 🐳 Docker 실행 방법

### 1) 이미지 빌드
```bash
docker build -t opensource-lotto:dev .
```

### 2) 컨테이너 실행
```bash
docker run -p 8000:8000 opensource-lotto:dev
```

→ 이후 웹 브라우저에서 접속:
```
http://127.0.0.1:8000
```

---

## 🐳 Docker Compose 실행 (선택)

```bash
docker compose up --build
```

종료는:
```bash
docker compose down
```

---

## 👤 관리자 페이지 (Admin)

```
http://127.0.0.1:8000/admin
```

관리자 계정 생성:
```bash
python manage.py createsuperuser
```


