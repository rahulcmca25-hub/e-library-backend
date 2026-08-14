from django.urls import path

from .views import (
    BorrowBookView,
    ReturnBookView,
    BorrowHistoryView,
    OverdueBooksView,
)


urlpatterns = [

    path(
        "borrow/",
        BorrowBookView.as_view(),
        name="borrow-book"
    ),

    path(
        "return/<int:pk>/",
        ReturnBookView.as_view(),
        name="return-book"
    ),

    path(
        "history/",
        BorrowHistoryView.as_view(),
        name="borrow-history"
    ),

    path(
        "overdue/",
        OverdueBooksView.as_view(),
        name="overdue-books"
    ),
]