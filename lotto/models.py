from django.db import models

class LottoTicket(models.Model):
    name = models.CharField(max_length=50)
    numbers = models.CharField(max_length=50)   # "1-5-12-21-34-45"
    match_status = models.CharField(max_length=10, default="미추첨")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.name} ({self.numbers}) - {self.match_status}"

class WinningNumber(models.Model):
    numbers = models.CharField(max_length=50)   # 유일 1행 개념
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Winning: {self.numbers}"
