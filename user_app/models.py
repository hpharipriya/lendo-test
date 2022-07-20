from django.db import models
from django.utils import timezone

from django.db import models
import uuid


class AdditionResult(models.Model):
    answer = models.IntegerField(default=0)

