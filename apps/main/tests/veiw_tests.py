from ddf import G
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.main.models import Question


class TestIndexView(TestCase):
    def setUp(self):
        self.question = G(Question, text="Two Sum", number=1, solved=True)

    def test_get_context_data(self):
        question = G(Question, text="Two Sum II", number=2)
        context_keys = ["questions", "practice_questions", "question_count", "solved_count"]

        response = self.client.get(reverse("main:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/index.html")

        for key in context_keys:
            self.assertIn(key, response.context)

        self.assertEqual(len(response.context["questions"]), 2)
        self.assertEqual(response.context["question_count"], 2)
        self.assertEqual(response.context["solved_count"], 1)

        q = response.context["questions"][1]
        self.assertEqual(q, question)
        self.assertEqual(q.text, "two sum ii")
        self.assertEqual(q.number, 2)
        self.assertEqual(q.solved, False)
        self.assertEqual(q.practice_count, 0)


class TestMarkQuestionSolvedView(TestCase):
    def setUp(self):
        self.question = G(Question, text="Two Sum", number=1, solved=False)

    def test_get(self):
        response = self.client.get(reverse("main:mark_solved", kwargs={"id": self.question.id}))
        self.assertEqual(response.status_code, 200)
        self.question.refresh_from_db()
        self.assertTrue(self.question.solved)


class TestMarkQuestionPracticedView(TestCase):
    def setUp(self):
        self.question = G(Question, text="Two Sum", number=1, practice_count=0)

    def test_get(self):
        response = self.client.get(reverse("main:mark_practiced", kwargs={"id": self.question.id}))
        self.assertEqual(response.status_code, 200)
        self.question.refresh_from_db()
        self.assertEqual(self.question.practice_count, 1)
        self.assertEqual(self.question.solved, True)
        self.assertEqual(self.question.last_practiced.date(), timezone.now().date())
