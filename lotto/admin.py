from django.contrib import admin
from .models import LottoTicket, WinningNumber

@admin.register(LottoTicket)
class LottoTicketAdmin(admin.ModelAdmin):
    list_display = ('name', 'numbers', 'match_status', 'created_at')
    search_fields = ('name', 'numbers')

@admin.register(WinningNumber)
class WinningNumberAdmin(admin.ModelAdmin):
    list_display = ('numbers', 'created_at')
