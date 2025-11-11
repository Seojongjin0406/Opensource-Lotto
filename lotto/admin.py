from django.contrib import admin
from .models import DrawRound, WinningSet, UserTicket

@admin.register(DrawRound)
class DrawRoundAdmin(admin.ModelAdmin):
    list_display = ("round_no", "draw_date")
    search_fields = ("round_no",)

@admin.register(WinningSet)
class WinningSetAdmin(admin.ModelAdmin):
    list_display = ("round", "numbers", "bonus", "created_at")
    search_fields = ("round__round_no", "numbers")

@admin.register(UserTicket)
class UserTicketAdmin(admin.ModelAdmin):
    list_display = ("round", "name", "numbers", "result_rank", "created_at")
    list_filter = ("result_rank", "round")
    search_fields = ("name", "numbers")
