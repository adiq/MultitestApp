from django.db import models
from django.utils import timezone


class Test(models.Model):
    title = models.CharField(max_length=150, blank=False)
    created_at = models.DateTimeField(default=timezone.now())


class Question(models.Model):
    question = models.TextField(blank=False)
    test = models.ForeignKey(Test)


class Answer(models.Model):
    answer = models.CharField(max_length=200, blank=False)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question)