from django.db import models

# Create your models here.
from datetime import timedelta
from django.db import models

BORROW_DURATION_CHOICES = (
    (timedelta(days=1), 'One day'),
    (timedelta(days=3), 'Three days'),
    (timedelta(days=7), 'One week'),
    (timedelta(days=30), 'One month'),
)


class Book(models.Model):
    name = models.CharField(max_length=50)
    author = models.ForeignKey('User', on_delete=models.CASCADE, null=False)
    publish_date = models.DateField(auto_now_add=True)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE, null=False)


class Genre(models.Model):
    name = models.CharField(max_length=50)


class User(models.Model):
    username = models.SlugField()
    email = models.EmailField()
    address = models.TextField()
    borrowed_books = models.ManyToManyField(Book, through='Borrow')

    def publish_book(self, book_name, genre):
        return NotImplemented


class Borrow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=False)
    borrow_time = models.DateTimeField(auto_now_add=True)
    duration = models.DurationField(choices=BORROW_DURATION_CHOICES, null=False, db_index=True)
    number = models.IntegerField(default=0)
