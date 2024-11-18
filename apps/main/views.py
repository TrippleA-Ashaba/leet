from django.views.generic import TemplateView

from .models import Question


class IndexView(TemplateView):
    model = Question
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["questions"] = self.model.objects.prefetch_related("topics").all()
        context["practice_questions"] = self.get_practice_questions()
        return context

    def get_practice_questions(self):
        questions = self.model.get_practice_questions()
        return questions
