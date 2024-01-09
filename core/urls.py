from django.urls import path
from .views import Home_View, AboutView, BookByCategory_View

urlpatterns = [
    path('', Home_View.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('category/<slug:category_slug>/', BookByCategory_View.as_view(), name='books_by_category'),
]
