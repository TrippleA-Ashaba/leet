from django.views.generic import TemplateView, View
from django_htmx.http import HttpResponseClientRefresh
from loguru import logger

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
            question.mark_solved()
        except self.model.DoesNotExist:
            logger.error(f"Question - {question_id} does not exist.")
            return HttpResponseClientRefresh()
        return HttpResponseClientRefresh()


class MarkQuestionPracticedView(View):
    model = Question

    def get(self, request, *args, **kwargs):
        question_id = kwargs.get("id")
        try:
            question = self.model.objects.get(id=question_id)
            question.mark_practiced()
        except self.model.DoesNotExist:
            logger.error(f"Question - {question_id} does not exist.")
            return HttpResponseClientRefresh()
        return HttpResponseClientRefresh()
