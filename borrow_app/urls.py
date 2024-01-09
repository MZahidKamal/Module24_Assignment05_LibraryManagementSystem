from django.urls import path
from .views import BorrowBook_View, ReturnBook_View

app_name = 'borrow_app'
urlpatterns = [
    path('borrow/<slug:book_slug>/', BorrowBook_View.as_view(), name='borrow_book'),
    path('return/<slug:borrow_slug>/', ReturnBook_View.as_view(), name='return_book'),
]
