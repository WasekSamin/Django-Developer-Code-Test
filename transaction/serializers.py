from rest_framework import serializers
from .models import Transaction, TransactionHistory


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"
        depth = 1


class TransactionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionHistory
        fields = "__all__"
        depth = 2