from datetime import timedelta

from author.decorators import with_author
from django.db import models
from django.db.models import Q
from django.utils import timezone
from model_utils.models import TimeStampedModel
from taggit.managers import TaggableManager


@with_author
class Question(TimeStampedModel):
    class Difficulty(models.TextChoices):
        EASY = "easy"
        MEDIUM = "medium"
        HARD = "hard"

    class Meta:
        verbose_name = "question"
        verbose_name_plural = "questions"
        unique_together = ("text", "author")
        ordering = ("number", "difficulty")

    text = models.CharField(max_length=255)
    difficulty = models.CharField(
        choices=Difficulty.choices,
        default=Difficulty.EASY,
        max_length=10,
    )
    number = models.PositiveIntegerField(
        verbose_name="leetcode number",
        null=True,
        blank=True,
        help_text="Leetcode problem number",
    )
    url = models.URLField(null=True, blank=True)
    topics = TaggableManager()
    practice_count = models.PositiveIntegerField(default=0)
    last_practiced = models.DateTimeField(null=True, blank=True)

    @classmethod
    def get_practice_questions(cls, question_count=5):
        one_week_ago = timezone.now() - timedelta(days=7)
        average_practice_count = Question.objects.aggregate(
            models.Avg("practice_count")
        )["practice_count__avg"]
        questions = Question.objects.filter(
            Q(last_practiced__lt=one_week_ago)
            | Q(last_practiced__isnull=True)
            | Q(practice_count__lte=average_practice_count)
        )

    def save(self, *args, **kwargs):
        self.text = self.text.lower()
        self.difficulty = self.difficulty.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.grind_num} - {self.text}"


@with_author
class Answer(TimeStampedModel):
    class Meta:
        verbose_name = "answer"
        verbose_name_plural = "answers"

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return f"{self.question} - {self.text}"
