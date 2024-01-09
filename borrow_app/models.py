from django.db import models
from django.utils.text import slugify

from user_app.models import UserProfile
from book_app.models import Book

# Create your models here.
PAYMENT_STATUS_CHOICES = [
    ('Payment Completed', 'PAID'),
    ('Refund Completed', 'REFUNDED'),
]

class Borrow(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowing_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='PAID')
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)

    def __str__(self):
        return f'{self.user_profile.user.username} borrowed {self.book.title}'

    def save(self, *args, **kwargs):
        is_new = self.id is None  # Check if this is a new instance
        super().save(*args, **kwargs)
        if is_new and not self.slug:  # if a new instance and no slug defined
            self.slug = slugify(f'{self.id}-{self.user_profile.user.username}-{self.book.title}-{self.borrowing_date}')
            super().save(update_fields=['slug'])
