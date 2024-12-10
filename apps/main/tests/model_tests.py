import time_machine
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from ddf import G
from django.test import TestCase
from django.utils import timezone

from apps.main.models import Question


class TestQuestionModel(TestCase):
    def test_question_creation_succeeds(self):
        question = G(Question, text="Test Question")
        self.assertEqual(question.text, "test question")
        self.assertEqual(question.difficulty, "easy")
        self.assertEqual(question.practice_count, 0)
        self.assertEqual(question.last_practiced, None)

    @time_machine.travel("2024-11-01")
    def test_get_a_week_later_practice_questions(self):
        today = timezone.now()
        question = G(Question, text="Test Question", difficulty="easy", last_practiced=today)

        # Move forward 1 week
        with time_machine.travel(today + relativedelta(days=7)):
            # create a few questions for current date
            for _ in range(10):
                G(Question, last_practiced=timezone.now())

            practice_questions = Question.get_practice_questions()

            qtn = practice_questions[0]

            self.assertEqual(len(practice_questions), 1)
            self.assertEqual(qtn, question)
            self.assertEqual(qtn.last_practiced, today)
            self.assertEqual(today.date(), parse("2024-11-01").date())
            self.assertEqual(qtn.modified.date(), parse("2024-11-01").date())

    def test_get_default_practice_questions_succeeds(self):
        one_weeks_ago = timezone.now() - relativedelta(days=7)
        two_weeks_ago = timezone.now() - relativedelta(days=14)
        for _ in range(10):
            G(Question, last_practiced=one_weeks_ago)

        # A question that was last practiced 2 weeks ago
        question = G(Question, text="Test Question", difficulty="easy", last_practiced=two_weeks_ago)

        practice_questions = Question.get_practice_questions()

        self.assertEqual(len(practice_questions), 5)
        self.assertIn(question, practice_questions)

    def test_get_a_number_of_practice_questions_succeeds(self):
        one_weeks_ago = timezone.now() - relativedelta(days=7)
        # One week old questions
        for _ in range(10):
            G(Question, last_practiced=one_weeks_ago)

        # Get 3 practice questions
        practice_questions = Question.get_practice_questions(question_count=7)

        self.assertEqual(len(practice_questions), 7)
