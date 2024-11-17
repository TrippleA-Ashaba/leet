from auditlog.registry import auditlog
from author.decorators import with_author
from django.contrib.auth.models import AbstractUser


@with_author
class User(AbstractUser):
    pass


# Register the model with auditlog
auditlog.register(User)
