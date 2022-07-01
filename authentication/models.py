from django.db import models
from uuid import uuid4
from django.utils import timezone


class User(models.Model):
    uid = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    username = models.CharField(max_length=120)
    mobile_number = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ("-created_at", )

    def __str__(self):
        return str(self.mobile_number)

    # Check if user already exists
    def check_for_user_exists(self, mobile_number):
        try:
            # If user exists, return True
            User.objects.get(mobile_number=mobile_number)
        except:
            # If user does not exists, return False
            return False
        else:
            return True

    # Returns user obj
    def get_user_obj(self, mobile_number):
        try:
            user_obj = User.objects.get(mobile_number=mobile_number)
        except User.DoesNotExist:
            return None
        else:
            return user_obj

    # Returns true if it is a number, else returns false
    def check_for_number_format(self, number):
        try:
            int(number)
        except ValueError:
            return False
        else:
            return True