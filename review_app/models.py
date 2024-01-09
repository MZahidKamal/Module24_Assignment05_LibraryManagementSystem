from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from user_app.models import UserProfile
from book_app.models import Book


# Create your models here.
class BookReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    review_text = models.TextField()
    review_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.book.title}"
