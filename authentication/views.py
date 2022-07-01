from transaction.models import TransactionHistory
from .models import User
from .serializers import UserSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class UserList(APIView):
    def get(self, request, format=None):
        snippets = User.objects.all()
        serializer = UserSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        resp_msg = {
            "error": True
        }

        username = request.data.get("username", None)
        mobile_number = request.data.get("mobile_number", None)

        if username is not None and mobile_number is not None and \
                len(username.strip()) > 0 and len(mobile_number.strip()) > 0:
            username = username.strip()
            mobile_number = mobile_number.strip()

            # Check if mobile number is in number format
            mobile_in_number_format = User.check_for_number_format(
                self, mobile_number)

            if not mobile_in_number_format:
                # If it is not a number, returns error response
                resp_msg = {
                    "error": True,
                    "invalid_mobile_number_format": True
                }
                return Response(resp_msg)

            user_exist = User.check_for_user_exists(self, mobile_number)

            # If user already exists, return error response
            if user_exist:
                resp_msg = {
                    "error": True,
                    "user_already_exists": True
                }
                return Response(resp_msg)

            # If user does not exist, create a new one
            user_obj = User(
                username=username,
                mobile_number=mobile_number
            )
            user_obj.save()

            transaction_hist_obj, created = TransactionHistory.objects.get_or_create(
                user=user_obj
            )

            resp_msg = {
                "error": False,
                "user_created_success": True,
                "transaction_history_created": True,
                "user_obj": {
                    "uid": user_obj.uid,
                    "username": user_obj.username,
                    "mobile_number": user_obj.mobile_number,
                    "created_at": user_obj.created_at
                },
                "transaction_history_obj": {
                    "uid": transaction_hist_obj.uid,
                    "money_amount": transaction_hist_obj.money_amount,
                    "created_at": transaction_hist_obj.created_at
                }
            }

        return Response(resp_msg)


class UserDetail(APIView):
    def get_object(self, uid):
        try:
            return User.objects.get(uid=uid)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, uid, format=None):
        snippet = self.get_object(uid)
        serializer = UserSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, uid, format=None):
        snippet = self.get_object(uid)
        serializer = UserSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uid, format=None):
        snippet = self.get_object(uid)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
