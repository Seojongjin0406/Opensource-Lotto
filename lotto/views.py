import random
from typing import List

from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import DrawRound, WinningSet, UserTicket


def _normalize(s: str) -> List[int]:
    """
    '1-2-3-4-5-6' 또는 '1,2,3,4,5,6' 형태를 정수 리스트(오름차순)로 변환/검증
    """
    nums = [int(x) for x in s.replace(",", "-").split("-") if x.strip()]
    if len(nums) != 6:
        raise ValueError("번호는 정확히 6개여야 합니다.")
    if any(n < 1 or n > 45 for n in nums):
        raise ValueError("번호는 1~45 범위여야 합니다.")
    if len(set(nums)) != 6:
        raise ValueError("중복 없이 6개여야 합니다.")
    return sorted(nums)


def _generate_auto_numbers() -> str:
    """1~45 중 6개 자동 추출 후 'a-b-c-d-e-f' 문자열로 반환"""
    return "-".join(str(x) for x in sorted(random.sample(range(1, 46), 6)))


def _grade(user_nums: List[int], win_nums: List[int], bonus: int) -> str:
    hit = len(set(user_nums) & set(win_nums))
    if hit == 6:
        return "1등"
    if hit == 5 and bonus in user_nums:
        return "2등"
    if hit == 5:
        return "3등"
    if hit == 4:
        return "4등"
    if hit == 3:
        return "5등"
    return "미당첨"


def home(request):
    latest = DrawRound.objects.order_by("-round_no").first()
    ctx = {"latest_round": latest}
    return render(request, "home.html", ctx)


def purchase_ticket(request):
    """
    구매 페이지: 수동/자동 입력 처리.
    - 템플릿: purchase_ticket.html
    """
    rounds = DrawRound.objects.order_by("-round_no")

    if request.method == "POST":
        # 폼 값 취득
        round_no_raw = request.POST.get("round_no")
        name = (request.POST.get("name") or "").strip()
        mode = request.POST.get("mode", "auto")  # 'auto' or 'manual'

        # 기본 검증
        if not round_no_raw or not round_no_raw.isdigit():
            messages.error(request, "회차를 올바르게 선택하세요.")
            return render(request, "purchase_ticket.html", {"rounds": rounds})

        if not name:
            messages.error(request, "이름을 입력하세요.")
            return render(request, "purchase_ticket.html", {"rounds": rounds})

        round_no = int(round_no_raw)

        try:
            rd = DrawRound.objects.get(round_no=round_no)

            if mode == "manual":
                # number input name이 동일한 6개 필드라면 request.POST.getlist("numbers") 사용
                # (예: <input name="numbers"> * 6)
                raw = "-".join(request.POST.getlist("numbers"))
                nums = _normalize(raw)
                numbers = "-".join(str(x) for x in nums)
            else:
                numbers = _generate_auto_numbers()

            UserTicket.objects.create(round=rd, name=name, numbers=numbers)
            messages.success(request, "구매가 완료되었습니다.")
            return redirect("my_results")

        except DrawRound.DoesNotExist:
            messages.error(request, "존재하지 않는 회차입니다.")
        except IntegrityError:
            messages.error(request, "같은 회차에서 동일 번호로 이미 구매했습니다.")
        except Exception as e:
            messages.error(request, f"오류: {e}")

    return render(request, "purchase_ticket.html", {"rounds": rounds})


def my_results(request):
    """
    내 결과 페이지: 최신 회차에 당첨번호가 있으면 미추첨 티켓 재채점.
    - 템플릿: my_results.html
    """
    latest = DrawRound.objects.order_by("-round_no").first()

    if latest and hasattr(latest, "winning_set"):
        ws = latest.winning_set
        win_nums = [int(x) for x in ws.numbers.split("-")]
        bonus = ws.bonus

        # 아직 '미추첨'인 최신 회차 티켓만 일괄 업데이트
        qs = UserTicket.objects.filter(round=latest, result_rank="미추첨")
        for t in qs:
            user_nums = [int(x) for x in t.numbers.split("-")]
            t.result_rank = _grade(user_nums, win_nums, bonus)
            t.save(update_fields=["result_rank"])

    tickets = UserTicket.objects.order_by("-created_at")[:20]
    return render(request, "my_results.html", {"tickets": tickets, "latest": latest})


def draw_winning_numbers(request):
    """
    당첨번호 추첨(관리자 대시보드의 버튼에서 POST로 호출)
    - 성공/실패 메시지 후 admin_dashboard로 리다이렉션
    """
    if request.method == "POST":
        round_no_raw = request.POST.get("round_no")
        if not round_no_raw or not round_no_raw.isdigit():
            messages.error(request, "회차를 올바르게 선택하세요.")
            return redirect("admin_dashboard")

        round_no = int(round_no_raw)
        try:
            rd = DrawRound.objects.get(round_no=round_no)
        except DrawRound.DoesNotExist:
            messages.error(request, "존재하지 않는 회차입니다.")
            return redirect("admin_dashboard")

        if hasattr(rd, "winning_set"):
            messages.warning(request, "이미 추첨되었습니다. 재추첨 불가.")
            return redirect("admin_dashboard")

        # 본번호 6개 + 보너스 1개
        main = sorted(random.sample(range(1, 46), 6))
        remain = [x for x in range(1, 46) if x not in main]
        bonus = random.choice(remain)

        WinningSet.objects.create(
            round=rd,
            numbers="-".join(map(str, main)),
            bonus=bonus,
        )
        messages.success(request, f"{round_no}회차 당첨번호: {main} + 보너스({bonus})")

    return redirect("admin_dashboard")


def admin_dashboard(request):
    """
    관리자 대시보드: 최신 회차 상태/최근 티켓 목록
    - 템플릿: admin_dashboard.html
    """
    latest = DrawRound.objects.order_by("-round_no").first()
    recent = UserTicket.objects.order_by("-created_at")[:10]
    return render(request, "admin_dashboard.html", {"latest": latest, "recent": recent})
