Opensource Lotto Project

사용자는 로또 번호를 수동/자동으로 구매하고, 내 결과를 확인할 수 있습니다.
관리자는 회차별 당첨번호 추첨과 사용자 통계를 볼 수 있습니다. (Django + Bootstrap, Docker 지원)

기능

사용자: 이름 + 번호 6개(수동/자동)로 티켓 구매, 최신 회차에 대해 결과 확인

관리자: 회차 생성(초기화), 당첨번호(6개+보너스) 추첨, 전 사용자 티켓 등수/통계 확인

실행: 로컬(Python) 또는 Docker 컨테이너

1) 받는 방법 (GitHub)
A. Git로 클론(추천)
git clone https://github.com/Seojongjin0406/Opensource-Lotto.git
cd Opensource-Lotto

B. ZIP 다운로드

저장소 페이지 → 초록 Code 버튼 → Download ZIP

압축 해제 후 폴더로 이동

2) 로컬 실행 (Python)
요구사항

Python 3.10+ (권장 3.11)

pip

가상환경 만들기 & 패키지 설치
Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate
pip install -r requirements.txt

macOS / Linux
python3 -m venv .venv
source ./.venv/bin/activate
pip install -r requirements.txt

DB 마이그레이션
python manage.py migrate

(선택) 초기 회차(1~5) 생성
python manage.py shell -c "from lotto.models import DrawRound; [DrawRound.objects.get_or_create(round_no=i) for i in range(1,6)]"

관리자 계정 만들기
python manage.py createsuperuser
# 안내에 따라 아이디/이메일/비밀번호 입력

개발 서버 실행
python manage.py runserver

접속 주소 & 주요 URL

앱 홈: http://127.0.0.1:8000/

로또 구매(사용자): http://127.0.0.1:8000/buy/

내 결과: http://127.0.0.1:8000/results/

관리자 대시보드(당첨번호 추첨/통계): http://127.0.0.1:8000/results-admin/

Django Admin: http://127.0.0.1:8000/admin/ (위에서 만든 관리자 계정으로 로그인)

관리자 대시보드에서 회차 선택 후 추첨 버튼을 누르면 당첨번호가 생성되고,
사용자의 미추첨 티켓은 내 결과 페이지에서 자동으로 등수가 계산됩니다.

3) Docker 로 실행
A. Dockerfile로 직접 빌드/실행
# 이미지 빌드
docker build -t opensource-lotto:dev .

# 컨테이너 실행 (포트 매핑: 호스트 8000 → 컨테이너 8000)
docker run -d --name lotto_dev -p 8000:8000 opensource-lotto:dev


초기 설정(마이그레이션/관리자/회차)은 컨테이너 내부에서 1회 실행:

docker exec -it lotto_dev bash

python manage.py migrate
python manage.py createsuperuser
python manage.py shell -c "from lotto.models import DrawRound; [DrawRound.objects.get_or_create(round_no=i) for i in range(1,6)]"
exit


접속: http://localhost:8000

정리:

docker stop lotto_dev
docker rm lotto_dev

B. Docker Compose (선택)

docker-compose.yml이 포함되어 있습니다.

docker compose up --build -d
# 초기 설정 필요하면:
docker compose exec web bash -lc "python manage.py migrate && python manage.py createsuperuser"
docker compose exec web bash -lc "python manage.py shell -c \"from lotto.models import DrawRound; [DrawRound.objects.get_or_create(round_no=i) for i in range(1,6)]\""


정리:

docker compose down
