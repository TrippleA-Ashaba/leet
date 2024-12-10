from author.decorators import with_author
from dateutil.relativedelta import relativedelta
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
        unique_together = ("text", "number")
        ordering = ("created", "id")

    text = models.CharField(max_length=255)
    difficulty = models.CharField(
        choices=Difficulty.choices,
        default=Difficulty.EASY,
        max_length=10,
    )
    number = models.PositiveIntegerField(
        verbose_name="leetcode number",
        help_text="Leetcode problem number",
        unique=True,
    )
    url = models.URLField(null=True, blank=True)
    topics = TaggableManager()
    practice_count = models.PositiveIntegerField(default=0)
    last_practiced = models.DateTimeField(null=True, blank=True)
    solved = models.BooleanField(default=False)

    @classmethod
    def get_practice_questions(self, queryset=None, question_count=5):
        one_week_ago = timezone.now() - relativedelta(weeks=1)
        filter_set = Q(last_practiced__lt=one_week_ago) | Q(
            last_practiced__isnull=True,
            modified__lt=one_week_ago,
            solved=True,
        )

        if queryset is None:
            queryset = Question.objects.all()

        return (
            queryset.filter(filter_set)
            .order_by("last_practiced", "practice_count")
            .prefetch_related("topics")[:question_count]
        )

    def mark_solved(self):
        if not self.solved:
            self.solved = True
        else:
            self.solved = False
        self.save()

    def mark_practiced(self):
        self.practice_count += 1
        self.last_practiced = timezone.now()
        if not self.solved:
            self.solved = True
        self.save()

    def save(self, *args, **kwargs):
        self.text = self.text.lower()
        self.difficulty = self.difficulty.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.number} - {self.text}"


@with_author
class Answer(TimeStampedModel):
    class Meta:
        verbose_name = "answer"
        verbose_name_plural = "answers"

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return f"{self.question} - {self.text}"
