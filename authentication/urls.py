from django.urls import path

from .views import (
    UserList, UserDetail
)


app_name = "user"
urlpatterns = [
    path("user-list/", UserList.as_view()),
    path("user-detail/<str:uid>/", UserDetail.as_view()),
]
