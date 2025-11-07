import random
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import LottoTicket, WinningNumber

def home(request):
    return render(request, "home.html")

def _normalize(numbers):
    return sorted(list(map(int, numbers.split("-"))))

def _generate_auto_numbers():
    nums = sorted(random.sample(range(1, 46), 6))
    return "-".join(map(str, nums))

def _grade(user_nums, win_nums):
    match = len(set(user_nums) & set(win_nums))
    if match == 6: return "1등"
    if match == 5: return "2등"
    if match == 4: return "3등"
    if match == 3: return "4등"
    return "미당첨"

def buy_lotto(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        mode = request.POST.get("mode", "manual")

        if not name:
            messages.error(request, "이름을 입력하세요.")
            return redirect("buy_lotto")

        if mode == "auto":
            numbers = _generate_auto_numbers()
        else:
            picks = [request.POST.get(f"n{i}") for i in range(1,7)]
            try:
                picks = list(map(int, picks))
            except:
                messages.error(request, "숫자 입력이 올바르지 않습니다.")
                return redirect("buy_lotto")
            if len(set(picks)) != 6 or not all(1 <= x <= 45 for x in picks):
                messages.error(request, "1~45 사이의 중복 없는 6개를 선택하세요.")
                return redirect("buy_lotto")
            numbers = "-".join(map(str, sorted(picks)))

        LottoTicket.objects.create(name=name, numbers=numbers, match_status="미추첨")
        return redirect("results_user")

    return render(request, "buy_lotto.html")

def results_user(request):
    tickets = LottoTicket.objects.order_by("-created_at")[:10]
    win = WinningNumber.objects.order_by("-created_at").first()

    if win:
        win_list = _normalize(win.numbers)
        for t in tickets:
            if t.match_status == "미추첨":
                user_list = _normalize(t.numbers)
                t.match_status = _grade(user_list, win_list)
                t.save()

    return render(request, "results_user.html", {"tickets": tickets, "winning": win})

def admin_draw(request):
    if request.method == "POST":
        if WinningNumber.objects.first():
            messages.warning(request, "이미 당첨번호가 존재합니다. 재추첨 불가.")
            return redirect("results_admin")
        numbers = _generate_auto_numbers()
        WinningNumber.objects.create(numbers=numbers)
        messages.success(request, f"당첨번호가 생성되었습니다: {numbers}")
        return redirect("results_admin")

    return render(request, "results_admin.html", {
        "winning": WinningNumber.objects.first(),
        "tickets": LottoTicket.objects.order_by("-created_at")[:20],
    })

def results_admin(request):
    win = WinningNumber.objects.first()
    tickets = LottoTicket.objects.order_by("-created_at")[:50]

    if win:
        win_list = _normalize(win.numbers)
        for t in tickets:
            user_list = _normalize(t.numbers)
            t.match_status = _grade(user_list, win_list)
            t.save()

    return render(request, "results_admin.html", {"winning": win, "tickets": tickets})
