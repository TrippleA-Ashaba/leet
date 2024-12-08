from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import TemplateView, View
from django_htmx.http import HttpResponseClientRedirect

from .models import Question


class IndexView(TemplateView):
    model = Question
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questions = self.model.objects.prefetch_related("topics").all()
        context["questions"] = questions
        context["practice_questions"] = self.model.get_practice_questions(queryset=questions)
        context["question_count"] = len(questions)
        context["solved_count"] = questions.filter(solved=True).count()
        return context


class MarkQuestionSolvedView(View):
    model = Question

    def get(self, request, *args, **kwargs):
        question_id = kwargs.get("id")
        try:
            question = self.model.objects.get(id=question_id)
            if not question.solved:
                question.solved = True
            else:
                question.solved = False
            question.save()
        except self.model.DoesNotExist:
            return HttpResponseClientRedirect(redirect("main:index"))
        return HttpResponseClientRedirect(redirect("main:index"))


class MarkQuestionPracticedView(View):
    model = Question

    def get(self, request, *args, **kwargs):
        question_id = kwargs.get("id")
        try:
            question = self.model.objects.get(id=question_id)
            question.practice_count += 1
            question.last_practiced = timezone.now()
            if not question.solved:
                question.solved = True
            question.save()
        except self.model.DoesNotExist:
            return HttpResponseClientRedirect(redirect("main:index"))
        return HttpResponseClientRedirect(redirect("main:index"))
