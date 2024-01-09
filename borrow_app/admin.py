from django.contrib import admin
from .models import Borrow

# Register your models here.
@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
    readonly_fields = ('borrowing_date',)
    list_display = ('user_profile', 'book', 'borrowing_date',)
