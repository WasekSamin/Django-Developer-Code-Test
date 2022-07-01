from django.urls import path

from .views import (
    TransactionList, TransactionDetail,
    TransactionHistoryList, TransactionHistoryDetail,
)


app_name = "transaction"
urlpatterns = [
    path("transaction-list/", TransactionList.as_view()),
    path("transaction-detail/<str:uid>/", TransactionDetail.as_view()),
    path("transaction-history-list/", TransactionHistoryList.as_view()),
    path("transaction-history-detail/<str:mobile_number>/", TransactionHistoryDetail.as_view()),
]
