from django.urls import path

from .views import IndexView, MarkQuestionSolvedView

app_name = "main"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("mark-solved/", MarkQuestionSolvedView.as_view(), name="mark-solved"),
]
