# 🎯 Opensource Lotto Project

사용자는 로또 번호를 **수동 또는 자동으로 구매**하고, **내 결과 페이지에서 등수 확인**을 할 수 있습니다.  
관리자는 회차별 **당첨번호(6개 + 보너스)** 를 추첨하고, **사용자 통계**를 확인할 수 있습니다.  
*(Django + Bootstrap + Docker 지원)*

---

## ✅ 주요 기능

| 구분 | 기능 |
|-----|------|
| 사용자 | 이름 + 번호 6개 입력 또는 자동 생성하여 구매, 내 최근 결과 확인 |
| 관리자 | 회차 생성, 당첨번호 추첨, 사용자 티켓 등수/통계 확인 |
| 실행 방식 | Python 로컬 실행 또는 Docker 실행 가능 |

---

## 📥 설치 & 실행 방법

### 1) 프로젝트 다운로드

#### ✅ Git Clone (추천)

git clone https://github.com/Seojongjin0406/Opensource-Lotto.git
cd Opensource-Lotto
또는 ZIP 다운로드
GitHub → Code → Download ZIP

압축 해제 후 폴더로 이동


🖥 로컬 실행 (Python)
요구사항
Python 3.10 이상 (권장 3.11)

pip

① 가상환경 생성 & 패키지 설치
Windows (PowerShell)
powershell
코드 복사
python -m venv .venv
.\.venv\Scripts\Activate
pip install -r requirements.txt
macOS / Linux
bash
코드 복사
python3 -m venv .venv
source ./.venv/bin/activate
pip install -r requirements.txt
② 데이터베이스 초기화
bash
코드 복사
python manage.py migrate
③ 회차(1~5) 초기 생성 (선택)
bash
코드 복사
python manage.py shell -c "from lotto.models import DrawRound; [DrawRound.objects.get_or_create(round_no=i) for i in range(1,6)]"
④ 관리자 계정 생성
bash
코드 복사
python manage.py createsuperuser
⑤ 서버 실행
bash
코드 복사
python manage.py runserver

🌐 접속 URL 안내
주소	설명
http://127.0.0.1:8000/	홈 화면
http://127.0.0.1:8000/buy/	사용자 로또 구매
http://127.0.0.1:8000/results/	내 결과 확인
http://127.0.0.1:8000/results-admin/	관리자 대시보드
http://127.0.0.1:8000/admin/	Django Admin 로그인


🐳 Docker 실행
① 이미지 빌드
bash
코드 복사
docker build -t opensource-lotto:dev .
② 컨테이너 실행
bash
코드 복사
docker run -d --name lotto_dev -p 8000:8000 opensource-lotto:dev
③ 컨테이너 내부 초기 설정 (1회만)
bash
코드 복사
docker exec -it lotto_dev bash
python manage.py migrate
python manage.py createsuperuser
python manage.py shell -c "from lotto.models import DrawRound; [DrawRound.objects.get_or_create(round_no=i) for i in range(1,6)]"
exit
④ 서버 접속
→ http://localhost:8000
