from django.test import TestCase
from authentication.models import User


class TestUserModel(TestCase):
    def setUp(self):
        for i in range(9):
            User.objects.create(
                username=f"User{i}",
                mobile_number=f"{i+100000}"
            )

    def test_user_is_created(self):
        user_obj = User.objects.create(
            username="Sam",
            mobile_number="1234"
        )

        user_created = user_obj in User.objects.all()
        self.assertTrue(user_created)

    def test_check_for_user_exists(self):
        found_user = User.check_for_user_exists(self, "100001")

        self.assertTrue(found_user)

    def test_get_user_obj(self):
        user_obj = User.get_user_obj(self, "100001")

        self.assertIsNotNone(user_obj)
