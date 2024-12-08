from django.urls import path

from .views import IndexView, MarkQuestionPracticedView, MarkQuestionSolvedView

app_name = "main"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("mark-solved/<int:id>/", MarkQuestionSolvedView.as_view(), name="mark_solved"),
    path("mark-practiced/<int:id>/", MarkQuestionPracticedView.as_view(), name="mark_practiced"),
]
