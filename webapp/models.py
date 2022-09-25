import datetime

from django.contrib import admin
from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Performance(models.Model):
    code = models.CharField(max_length=6)
    name = models.CharField(max_length=32)
    rev_inc = models.DecimalField
    rev_inc_qoq = models.DecimalField
    np_inc = models.DecimalField
    np_inc_qoq = models.DecimalField
    roe = models.DecimalField
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.code + ',' + self.name

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Stock(models.Model):
    id = models.CharField(primary_key=True, max_length=6)
    name = models.CharField(max_length=32)
    xchg = models.CharField(max_length=2)

    @admin.display(
        boolean=True,
        ordering='code',
    )
    def __str__(self):
        return self.id + ',' + self.name + ',' + self.xchg
