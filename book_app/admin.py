from django.contrib import admin
from .models import Category, StarRating, Book

# Register your models here.
class Category_Admin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')

# class Book_Admin(admin.ModelAdmin):
#     prepopulated_fields = {'slug': ('title',)}
#     list_display = ('title', 'slug')

admin.site.register(Category, Category_Admin)
admin.site.register(StarRating)
admin.site.register(Book)
