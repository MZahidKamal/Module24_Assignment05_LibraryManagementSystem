from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import DetailView
from django.http import HttpResponseForbidden, HttpResponseRedirect
from .models import Book, Category
from review_app.models import BookReview
from review_app.forms import BookReview_Form
from borrow_app.models import Borrow
from user_app.models import UserProfile

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class BookDetails_View(DetailView):
    model = Book
    template_name = 'book_app/book_details.html'
    slug_url_kwarg = 'book_slug'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        book_reviews = BookReview.objects.filter(book=book)
        context['book_reviews'] = book_reviews
        context['form'] = BookReview_Form()
        return context

    def post(self, request, *args, **kwargs):
        form = BookReview_Form(request.POST)
        book = self.get_object()

        user_profile = request.user.userprofile
        user_borrowed_this_book = Borrow.objects.filter(user_profile=user_profile, book=book, return_date__isnull=False).exists()

        if user_borrowed_this_book and form.is_valid():
            new_review = form.save(commit=False)
            new_review.user = request.user
            new_review.book = book
            new_review.save()
        # return redirect('home')
        return self.get(request, *args, **kwargs)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
