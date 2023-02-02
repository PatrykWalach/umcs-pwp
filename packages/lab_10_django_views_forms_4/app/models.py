from __future__ import annotations

from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True)
    genre = models.CharField(max_length=100)


class Reader(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)


class Borrowing(models.Model):
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
