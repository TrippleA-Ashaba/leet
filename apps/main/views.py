from django.views.generic import TemplateView

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
