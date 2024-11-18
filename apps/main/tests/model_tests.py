from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from apps.main.models import Question


class TestQuestionModel(TestCase):
    def test_question_creation_succeeds(self):
        question = Question(text="Test Question", difficulty="easy")
        question.save()
        self.assertEqual(question.text, "test question")
        self.assertEqual(question.difficulty, "easy")
        self.assertEqual(question.practice_count, 0)
        self.assertEqual(question.last_practiced, None)

    def test_get_practice_questions_succeeds(self):
        two_weeks_ago = timezone.now() - timedelta(days=14)
        question = Question(text="Test Question", difficulty="easy", last_practiced=two_weeks_ago)
        question.save()
        practice_questions = Question.get_practice_questions()
        self.assertIn(question, practice_questions)
