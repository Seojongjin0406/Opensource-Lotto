import random
from typing import List

from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import DrawRound, WinningSet, UserTicket


def _normalize(s: str) -> List[int]:
    """'1-2-3-4-5-6' 또는 '1,2,3,4,5,6' -> 검증 후 오름차순 리스트"""
    nums = [int(x) for x in s.replace(",", "-").split("-") if x.strip()]
    if len(nums) != 6:
        raise ValueError("번호는 정확히 6개여야 합니다.")
    if any(n < 1 or n > 45 for n in nums):
        raise ValueError("번호는 1~45 범위여야 합니다.")
    if len(set(nums)) != 6:
        raise ValueError("중복 없이 6개여야 합니다.")
    return sorted(nums)


def _generate_auto_numbers() -> str:
    """1~45 중 6개 자동 추출 후 'a-b-c-d-e-f' 문자열"""
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
    return render(request, "home.html", {"latest": latest})


def purchase_ticket(request):
    """
    구매 페이지 (purchase_ticket.html)
    - 수동: n1~n6
    - 자동: 난수 6개
    """
    rounds = DrawRound.objects.order_by("-round_no")

    if request.method == "POST":
        round_no_raw = request.POST.get("round_no")
        name = (request.POST.get("name") or "").strip()
        mode = request.POST.get("mode", "auto")

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
                num_list = [
                    request.POST.get("n1", ""),
                    request.POST.get("n2", ""),
                    request.POST.get("n3", ""),
                    request.POST.get("n4", ""),
                    request.POST.get("n5", ""),
                    request.POST.get("n6", ""),
                ]
                raw = "-".join(num_list)
                nums = _normalize(raw)
                numbers = "-".join(map(str, nums))
            else:
                numbers = _generate_auto_numbers()

            UserTicket.objects.create(round=rd, name=name, numbers=numbers)
            messages.success(request, "구매가 완료되었습니다.")
            return redirect("results_user")

        except DrawRound.DoesNotExist:
            messages.error(request, "존재하지 않는 회차입니다.")
        except IntegrityError:
            messages.error(request, "같은 회차에서 동일 번호로 이미 구매했습니다.")
        except Exception as e:
            messages.error(request, f"오류: {e}")

    return render(request, "purchase_ticket.html", {"rounds": rounds})


def results_user(request):
    """
    사용자 결과 페이지 (my_results.html)
    - 최신 회차의 당첨번호가 있으면 '미추첨' 티켓들을 일괄 채점
    """
    latest_round = DrawRound.objects.order_by("-round_no").first()

    winning = None
    if latest_round and hasattr(latest_round, "winning_set"):
        ws = latest_round.winning_set
        winning = ws
        win_nums = [int(x) for x in ws.numbers.split("-")]
        bonus = ws.bonus

        for t in UserTicket.objects.filter(round=latest_round, result_rank="미추첨"):
            user_nums = [int(x) for x in t.numbers.split("-")]
            t.result_rank = _grade(user_nums, win_nums, bonus)
            t.save(update_fields=["result_rank"])

    tickets = UserTicket.objects.order_by("-created_at")[:20]
    return render(
        request,
        "my_results.html",
        {"tickets": tickets, "latest_round": latest_round, "winning": winning},
    )


def draw_winning_numbers(request):
    """
    관리자: 당첨번호 추첨 (POST) → results_admin 리다이렉트
    """
    if request.method == "POST":
        round_no_raw = request.POST.get("round_no")
        if not round_no_raw or not round_no_raw.isdigit():
            messages.error(request, "회차를 올바르게 선택하세요.")
            return redirect("results_admin")

        round_no = int(round_no_raw)
        try:
            rd = DrawRound.objects.get(round_no=round_no)
        except DrawRound.DoesNotExist:
            messages.error(request, "존재하지 않는 회차입니다.")
            return redirect("results_admin")

        if hasattr(rd, "winning_set"):
            messages.warning(request, "이미 추첨되었습니다. 재추첨 불가.")
            return redirect("results_admin")

        main = sorted(random.sample(range(1, 46), 6))
        remain = [x for x in range(1, 46) if x not in main]
        bonus = random.choice(remain)

        WinningSet.objects.create(
            round=rd,
            numbers="-".join(map(str, main)),
            bonus=bonus,
        )
        messages.success(request, f"{round_no}회차 당첨번호: {main} + 보너스({bonus})")

    return redirect("results_admin")


def admin_dashboard(request):
    """
    관리자 대시보드 (admin_dashboard.html)
    템플릿 기대 키: latest_round, winning, rounds, tickets
    """
    latest_round = DrawRound.objects.order_by("-round_no").first()
    winning = latest_round.winning_set if (latest_round and hasattr(latest_round, "winning_set")) else None
    rounds = DrawRound.objects.order_by("-round_no")
    tickets = UserTicket.objects.order_by("-created_at")[:20]

    return render(
        request,
        "admin_dashboard.html",
        {"latest_round": latest_round, "winning": winning, "rounds": rounds, "tickets": tickets},
    )
