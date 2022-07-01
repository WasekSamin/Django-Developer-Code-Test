from lib2to3.pgen2.parse import ParseError
from .models import Transaction, TransactionHistory
from authentication.models import User
from .serializers import TransactionSerializer, TransactionHistorySerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal, InvalidOperation
from dateutil.parser import parse
from dateutil.parser._parser import ParserError
from django.utils import timezone


class TransactionList(APIView):
    def get(self, request, format=None):
        snippets = Transaction.objects.all()
        serializer = TransactionSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionDetail(APIView):
    def get_object(self, uid):
        try:
            return Transaction.objects.get(uid=uid)
        except Transaction.DoesNotExist:
            raise Http404

    def get(self, request, uid, format=None):
        snippet = self.get_object(uid)
        serializer = TransactionSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, uid, format=None):
        snippet = self.get_object(uid)
        serializer = TransactionSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uid, format=None):
        snippet = self.get_object(uid)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TransactionHistoryList(APIView):
    def get(self, request, format=None):
        snippets = TransactionHistory.objects.all()
        serializer = TransactionHistorySerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        resp_msg = {
            "error": True
        }

        sender = request.data.get("user", None)
        transactions = request.data.get("transaction", None)

        if sender is not None and transactions is not None and len(transactions) > 0:
            sender_mobile_number = sender.get("mobile_number", None)

            if sender_mobile_number is not None and len(sender_mobile_number.strip()) > 0:
                sender_mobile_number = sender_mobile_number.strip()

                # Check if sender mobile number is in number format
                sender_mobile_in_number_format = User.check_for_number_format(
                    self, sender_mobile_number)

                # If sender_mobile_number is not a number, returns error response
                if not sender_mobile_in_number_format:
                    resp_msg = {
                        "error": True,
                        "invalid_mobile_number_format": True
                    }
                    return Response(resp_msg)

                # Getting transaction history obj
                trans_hist_obj = TransactionHistory.get_transaction_history_obj(
                    self, sender_mobile_number)

                if trans_hist_obj is None:
                    resp_msg = {
                        "error": True,
                        "user_not_found": True
                    }
                    return Response(resp_msg)

                # Appending given receiver mobile numbers, sent amount, and transfer_scheduled_time into a list
                receiver_obj_list = [
                    {
                        "receiver_mobile_number": transaction.get("receiver").get("mobile_number").strip(),
                        "sent_amount": transaction.get("sent_amount").strip(),
                        "transfer_scheduled_time": transaction.get("transfer_scheduled_time")
                    } for transaction in transactions
                    if transaction.get("receiver", None).get("mobile_number", None) is not None and len(transaction.get("receiver", None).get("mobile_number", None).strip()) > 0
                    and transaction.get("sent_amount") is not None and len(transaction.get("sent_amount").strip()) > 0
                ]

                if len(receiver_obj_list) == 0:
                    resp_msg = {
                        "error": True,
                        "no_receiver_added": True
                    }
                    return Response(resp_msg)

                for rn in receiver_obj_list:
                    # Convert sent amount to decimal format
                    try:
                        sent_amount = Decimal(rn.get("sent_amount"))
                    except InvalidOperation:
                        # If sent amount is not a number, then continue loop to next object
                        continue
                    else:
                        receiver_mobile_number = rn.get(
                            "receiver_mobile_number")
                        transfer_scheduled_time = rn.get(
                            "transfer_scheduled_time", None)
                        # If sent amount is less or equal 0, then continue loop to next object
                        if sent_amount <= 0:
                            continue
                        
                        # Check if transfer_scheduled time is valid
                        if transfer_scheduled_time is not None:
                            try:
                                transfer_scheduled_time = parse(transfer_scheduled_time)
                            except ParserError:
                                continue

                        if trans_hist_obj.money_amount < sent_amount:
                            resp_msg = {
                                "error": True,
                                "not_enough_amount": True
                            }
                            return Response(resp_msg)

                        # Check if receiver mobile number is in number format
                        receiver_mobile_in_number_format = User.check_for_number_format(
                            self, receiver_mobile_number)

                        if not receiver_mobile_in_number_format:
                            continue

                        receiver_obj = User.get_user_obj(
                            self, receiver_mobile_number)

                        # If current receiver is None, then continue the loop and get the next receiver obj
                        if receiver_obj is None:
                            continue

                        transaction_obj = Transaction(
                            receiver=receiver_obj,
                            sent_amount=sent_amount,
                            transfer_scheduled_time=transfer_scheduled_time
                        )
                        transaction_obj.save()

                        trans_hist_obj.money_amount -= sent_amount
                        trans_hist_obj.save(update_fields=["money_amount"])

                        trans_hist_obj.transaction.add(transaction_obj.uid)

                # After transaction process
                resp_msg = {
                    "error": False,
                    "transaction_success": True,
                    "transaction_history_obj": {
                        "uid": trans_hist_obj.uid,
                        "money_amount": trans_hist_obj.money_amount
                    }
                }
                return Response(resp_msg)

        return Response(resp_msg)


#### Get user transaction history from user's mobile number ####
class TransactionHistoryDetail(APIView):
    def get_object(self, mobile_number):
        try:
            return TransactionHistory.objects.get(user__mobile_number=mobile_number)
        except TransactionHistory.DoesNotExist:
            raise Http404

    def get(self, request, mobile_number, format=None):
        snippet = self.get_object(mobile_number)
        serializer = TransactionHistorySerializer(snippet)
        return Response(serializer.data)

    def put(self, request, mobile_number, format=None):
        snippet = self.get_object(mobile_number)
        serializer = TransactionHistorySerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, mobile_number, format=None):
        snippet = self.get_object(mobile_number)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
