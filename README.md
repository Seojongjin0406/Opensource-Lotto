🎯 Opensource Lotto Project

사용자는 로또 번호를 수동 또는 자동으로 구매하고,
내 결과 확인 / 관리자 당첨번호 추첨 / 사용자 통계 확인을 할 수 있는 Django 기반 웹 서비스입니다.
(Django + Bootstrap UI + Docker 실행 지원)

✅ 주요 기능
구분	설명
사용자 기능	이름 + 번호 6개(수동/자동) 로또 구매, 최근 회차 내 구매 결과 확인
관리자 기능	회차 생성, 당첨 번호(6개 + 보너스) 추첨, 사용자 제출 내역 통계 확인
실행 방식	Python 로컬 실행 또는 Docker 컨테이너 실행 가능
🛠 설치 & 실행 방법
1) 프로젝트 다운로드
✅ Git Clone (추천)
git clone https://github.com/Seojongjin0406/Opensource-Lotto.git
cd Opensource-Lotto


또는
GitHub → Code → Download ZIP → 압축 해제 후 폴더 이동

🖥 로컬 실행 (Python 방식)
✅ 요구사항

Python 3.10 이상 (권장 3.11)

pip 설치 필요

① 가상환경 생성 & 활성화
Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate
pip install -r requirements.txt

macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

② 데이터베이스 초기화
python manage.py migrate

③ 관리자 계정 생성
python manage.py createsuperuser

④ 초기 회차 데이터 생성 (1~5회차)
python manage.py shell -c "from lotto.models import DrawRound; [DrawRound.objects.get_or_create(round_no=i) for i in range(1,6)]"

⑤ 서버 실행
python manage.py runserver

🌐 주요 접속 경로
주소	설명
http://127.0.0.1:8000
	홈 화면
http://127.0.0.1:8000/buy/
	사용자 로또 구매
http://127.0.0.1:8000/results/
	내 로또 결과 확인
http://127.0.0.1:8000/results-admin/
	관리자 통계 / 추첨 화면
http://127.0.0.1:8000/admin/
	Django Admin (관리자 로그인 필요)
🐳 Docker 실행
① 이미지 빌드
docker build -t opensource-lotto:dev .

② 컨테이너 실행
docker run -d --name lotto_dev -p 8000:8000 opensource-lotto:dev

③ 컨테이너 내부 설정 (최초 1회만)
docker exec -it lotto_dev bash
python manage.py migrate
python manage.py createsuperuser
python manage.py shell -c "from lotto.models import DrawRound; [DrawRound.objects.get_or_create(round_no=i) for i in range(1,6)]"
exit

④ 접속
http://localhost:8000

📌 참고

본 프로젝트는 오픈소스SW활용 수업 과제 제출용입니다.
