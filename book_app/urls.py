from django.urls import path
from .views import BookDetails_View

urlpatterns = [
    path('book/<slug:book_slug>/', BookDetails_View.as_view(), name='book_details'),
]
