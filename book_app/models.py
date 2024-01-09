from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class StarRating(models.Model):
    rating = models.CharField(max_length=5)

    def __str__(self):
        return self.rating


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    isbn = models.CharField(max_length=25)
    publisher = models.CharField(max_length=50)
    image = models.ImageField(upload_to='borrow_app/media/uploads/', blank=True, null=True)
    description = models.TextField(max_length=5000)
    reviews = models.ForeignKey(StarRating, on_delete=models.SET_NULL, null=True, blank=True)
    borrowing_price = models.DecimalField(max_digits=10, decimal_places=2)
    available_stock = models.PositiveIntegerField(default=0)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)

    def __str__(self):
        return f'{self.title} - {self.author}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(f'{self.id} - {self.title} - {self.author} - {self.isbn}')
            super().save(update_fields=['slug'])
