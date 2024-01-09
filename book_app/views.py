from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from django.http import HttpResponseForbidden, HttpResponseRedirect
from .models import Book, Category
from review_app.models import BookReview
from review_app.forms import BookReview_Form
from borrow_app.models import Borrow

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# class ReviewRequiredMixin(LoginRequiredMixin):
#     def dispatch(self, request, *args, **kwargs):
#         self.book = get_object_or_404(Book, slug=self.kwargs['book_slug'])
#         # borrowed_book = Borrow.objects.filter(user=request.user, book=self.book, return_date=not None).exists()
#         if not Borrow.objects.filter(user=request.user):
#             if Borrow.objects.filter()
#             return HttpResponseForbidden("You can't post a review without borrowing the book.")
#         return super().dispatch(request, *args, **kwargs)


# class ReviewRequiredMixin(LoginRequiredMixin):
#     def dispatch(self, request, *args, **kwargs):
#         self.book = get_object_or_404(Book, slug=self.kwargs['book_slug'])
#         borrowed_book = Borrow.objects.filter(
#             user=request.user,
#             book=self.book,
#             return_date__isnull=False  # Check for non-NULL return_date
#         ).exists()
#         if not borrowed_book:
#             return HttpResponseForbidden("You can't post a review without borrowing the book.")
#         return super().dispatch(request, *args, **kwargs)


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# class BookDetails_View(ReviewRequiredMixin, DetailView):
#     model = Book
#     template_name = 'book_app/book_details.html'
#     slug_url_kwarg = 'book_slug'        # the name of the kwarg in the URLconf
#     slug_field = 'slug'                 # the name of the slug field on the model
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['review_form'] = BookReview_Form()
#         return context
#
#     def post(self, request, *args, **kwargs):
#         form = BookReview_Form(request.POST)
#         if form.is_valid():
#             review = form.save(commit=False)
#             review.user = request.user
#             review.book = self.book
#             review.save()
#             return HttpResponseRedirect(self.request.path_info)
#         return self.get(request, *args, **kwargs)

class BookDetails_View(DetailView):
    model = Book
    template_name = 'book_app/book_details.html'
    slug_url_kwarg = 'book_slug'        # the name of the kwarg in the URLconf
    slug_field = 'slug'                 # the name of the slug field on the model

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['review_form'] = BookReview_Form()
    #     return context
    #
    # def post(self, request, *args, **kwargs):
    #     form = BookReview_Form(request.POST)
    #     if form.is_valid():
    #         review = form.save(commit=False)
    #         review.user = request.user
    #         review.book = self.book
    #         review.save()
    #         return HttpResponseRedirect(self.request.path_info)
    #     return self.get(request, *args, **kwargs)
