from django.db import models
from authentication.models import User
from django.utils import timezone
from uuid import uuid4


class Transaction(models.Model):
    uid = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    sent_amount = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    transfer_scheduled_time = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return str(self.uid)


# User transaction history
class TransactionHistory(models.Model):
    uid = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Sender
    money_amount = models.DecimalField(default=5000.0, max_digits=10, decimal_places=2) # By default, user got 5000 tk
    transaction = models.ManyToManyField(Transaction, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ("-created_at", )

    def __str__(self):
        return str(self.uid)

    # Transaction history obj
    def get_transaction_history_obj(self, mobile_number):
        try:
            transaction_hist_obj = TransactionHistory.objects.get(
                user__mobile_number=mobile_number)
        except TransactionHistory.DoesNotExist:
            return None
        else:
            return transaction_hist_obj
