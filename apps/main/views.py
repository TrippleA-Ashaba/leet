from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import TemplateView, View

from .models import Question


class IndexView(TemplateView):
    model = Question
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questions = self.model.objects.prefetch_related("topics").all()
        context["questions"] = questions
        context["practice_questions"] = self.model.get_practice_questions()
        context["question_count"] = questions.count()
        return context


class MarkQuestionSolvedView(View):
    model = Question

    def get(self, request, *args, **kwargs):
        print("Marking question as solved")
        question_id = request.GET.get("question_id")
        if question_id:
            question = self.model.objects.get(id=question_id)
            question.practice_count += 1
            question.last_practiced = timezone.now()
            question.save()

        return redirect("main:index")
