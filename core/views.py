# IMPORT SECTION
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from book_app.models import Category, Book

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CREATE VIEWS SECTION
class Home_View(TemplateView):
    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.all()
        context['categories'] = Category.objects.all()
        return context

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class BookByCategory_View(TemplateView):
    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs['category_slug']
        context['books'] = Book.objects.filter(category__slug=category_slug)
        context['categories'] = Category.objects.all()
        return context

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class AboutView(TemplateView):
    template_name = 'core/about.html'

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
