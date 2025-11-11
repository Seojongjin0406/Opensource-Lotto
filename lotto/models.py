from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class DrawRound(models.Model):
    round_no = models.PositiveIntegerField(unique=True, verbose_name="회차")
    draw_date = models.DateTimeField(default=timezone.now, verbose_name="추첨일")

    class Meta:
        db_table = "lotto_round"
        ordering = ["-round_no"]
        verbose_name = "추첨 회차"
        verbose_name_plural = "추첨 회차"

    def __str__(self):
        return f"{self.round_no}회차"


class WinningSet(models.Model):
    round = models.OneToOneField(
        DrawRound,
        on_delete=models.CASCADE,
        related_name="winning_set",
        verbose_name="회차",
    )
    numbers = models.CharField(max_length=30, verbose_name="본번호(정렬된 6개)")
    bonus = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(45)],
        verbose_name="보너스"
    )
    # Admin/뷰 어디서 생성해도 자동 세팅
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성 시각")

    class Meta:
        db_table = "lotto_winningnumber"
        verbose_name = "당첨번호 세트"
        verbose_name_plural = "당첨번호 세트"

    def __str__(self):
        return f"{self.round} : {self.numbers} + 보너스({self.bonus})"


class UserTicket(models.Model):
    round = models.ForeignKey(
        DrawRound, on_delete=models.CASCADE, related_name="tickets", verbose_name="회차"
    )
    name = models.CharField(max_length=30, verbose_name="이름")
    numbers = models.CharField(max_length=30, verbose_name="선택 번호(정렬된 6개)")

    result_rank = models.CharField(
        db_column="match_status",
        max_length=10,
        default="미추첨",
        verbose_name="등수/상태",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="구매 시각")

    class Meta:
        db_table = "lotto_lottoticket"
        unique_together = ("round", "name", "numbers")
        ordering = ["-created_at"]
        verbose_name = "사용자 티켓"
        verbose_name_plural = "사용자 티켓"

    def __str__(self):
        return f"[{self.round}] {self.name} : {self.numbers} ({self.result_rank})"
