from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=100)


class Reader(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)


class Borrowing(models.Model):
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
