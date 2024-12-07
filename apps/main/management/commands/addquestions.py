import json

from django.core.management.base import BaseCommand

from apps.main.models import Question


class Command(BaseCommand):
    help = "Add questions to the database"

    def handle(self, *args, **options):
        questions_file = "leet_questions.json"
        try:
            with open(questions_file) as f:
                data = json.load(f)
                not_added_questions = []

                for question in data:
                    try:
                        q = Question.objects.create(
                            number=question["number"],
                            text=question["text"],
                            difficulty=question["difficulty"],
                            url=question["url"],
                        )
                        q.topics.add(*question["topics"])
                    except Exception as e:
                        not_added_questions.append(question.get("number"))
                        self.stdout.write(self.style.ERROR(f"Error adding question: {e}"))
                        continue

                if not_added_questions:
                    self.stdout.write(
                        self.style.ERROR(f"Failed to add questions {len(not_added_questions)}: {not_added_questions}")
                    )
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File not found: '{questions_file}' "))
        else:
            self.stdout.write(self.style.SUCCESS("Successfully added questions"))
