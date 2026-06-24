from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'transaction_id',
            'user_id',
            'amount'
        ]

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Amount must be greater than 0."
            )

        if value < 10:
            raise serializers.ValidationError(
                "Minimum transaction amount is 10."
            )

        return value