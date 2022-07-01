from django.test import TestCase
from authentication.models import User
from .models import TransactionHistory, Transaction
from random import uniform


class TestTransactionHistoryModel(TestCase):
    def setUp(self):
        for i in range(9):
            user_obj = User.objects.create(
                username=f"User{i}",
                mobile_number=f"{i+100000}"
            )
            TransactionHistory.objects.create(
                user=user_obj
            )
    
    def test_send_transaction(self):
        trans_hist_obj = TransactionHistory.get_transaction_history_obj(self, "100000")
        number_of_transactions = trans_hist_obj.transaction.count()
        money_amount = trans_hist_obj.money_amount
        self.assertIsNotNone(trans_hist_obj)

        for i in range(1, 9):
            transfer_scheduled_time = "2022-06-30T23:46:34"
            sent_amount = round(uniform(10, 500))

            self.assertGreaterEqual(trans_hist_obj.money_amount, sent_amount)

            receiver_obj = User.get_user_obj(self, i+100000)

            self.assertIsNotNone(receiver_obj)

            trans_obj = Transaction(
                receiver=receiver_obj,
                sent_amount=sent_amount,
                transfer_scheduled_time=transfer_scheduled_time
            )
            trans_obj.save()

            self.assertTrue(trans_obj in Transaction.objects.all())

            trans_hist_obj.money_amount -= sent_amount
            trans_hist_obj.save(update_fields=["money_amount"])
            trans_hist_obj.transaction.add(trans_obj)
        
        self.assertLess(trans_hist_obj.money_amount, money_amount)
        self.assertGreater(trans_hist_obj.transaction.count(), number_of_transactions)

            
