from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'transaction_id',
        'user_id',
        'amount',
        'created_at'
    )

    search_fields = (
        'transaction_id',
        'user_id'
    )