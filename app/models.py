from django.db import models


class Transaction(models.Model):
    transaction_id = models.CharField(
        max_length=100,
        unique=True
    )

    user_id = models.CharField(
        max_length=100
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.transaction_id} - {self.user_id}"