from django.contrib import admin
from .models import BookReview

# Register your models here.
@admin.register(BookReview)
class BookReviewAdmin(admin.ModelAdmin):
    # readonly_fields = ('review_text', 'review_date')
    list_display = ('user', 'book', 'review_date')
