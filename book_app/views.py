from django.views import View
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from .models import Book, Category


class BookDetails_View(DetailView):
    model = Book
    template_name = 'book_app/book_details.html'
    slug_url_kwarg = 'book_slug'        # the name of the kwarg in the URLconf
    slug_field = 'slug'                 # the name of the slug field on the model
