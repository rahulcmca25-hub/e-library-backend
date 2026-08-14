from django.urls import path

from .views import (
    BookSummaryView,
    BookSummaryDetailView
)


urlpatterns = [

    path(
        "books/<int:pk>/summary/",
        BookSummaryView.as_view(),
        name="book-summary"
    ),

    path(
        "books/<int:pk>/summary/view/",
        BookSummaryDetailView.as_view(),
        name="book-summary-detail"
    ),

]