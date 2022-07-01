from django.contrib import admin

from .models import Transaction, TransactionHistory


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "uid", "receiver",
        "sent_amount", "transfer_scheduled_time"
    )


@admin.register(TransactionHistory)
class TransactionHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "uid", "user",
        "money_amount", "created_at"
    )
