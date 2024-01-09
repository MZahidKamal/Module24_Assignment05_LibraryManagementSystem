from datetime import date
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import View

from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string

from user_app.models import UserProfile
from book_app.models import Book
from .models import Borrow

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Create your views here.

def send_borrow_return_confirmation_email(user, subject, borrow, target_email, template_name):
    email_subject = subject
    message = render_to_string(template_name, {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'book': borrow.book.title,
        'amount': borrow.book.borrowing_price,
        'wallet_balance': user.userprofile.wallet_balance,
    })
    to_email = target_email
    send_email = EmailMultiAlternatives(email_subject, '', to=[to_email])
    send_email.attach_alternative(message, 'text/html')
    send_email.send()

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class BorrowBook_View(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        book = get_object_or_404(Book, slug=self.kwargs['book_slug'])
        user = request.user
        user_profile = UserProfile.objects.get(user=user)

        if book.available_stock <= 0:
            messages.error(request, 'Book stock is empty, please check again in few days.')
            return render(request, reverse_lazy('profile'))

        if user_profile.wallet_balance < book.borrowing_price:
            messages.error(request, 'Insufficient balance in wallet.')
            return render(request, reverse_lazy('profile'))

        user_profile.wallet_balance -= book.borrowing_price
        user_profile.save()
        book.available_stock -= 1
        book.save()

        borrow = Borrow.objects.create(
            user_profile=user_profile,
            book=book,
        )
        # Sending borrow confirmation email.
        send_borrow_return_confirmation_email(user, 'Book borrow Successful', borrow, user.email, 'borrow_app/borrow_confirmation_email.html')

        return redirect(reverse_lazy('profile'))

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class ReturnBook_View(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        borrow = get_object_or_404(Borrow, slug=self.kwargs['borrow_slug'])
        book = borrow.book
        user = request.user
        user_profile = borrow.user_profile

        if user_profile.user == user:

            user_profile.wallet_balance += book.borrowing_price
            user_profile.save()

            borrow.book.available_stock += 1
            borrow.book.save()

            borrow.return_date = date.today()
            borrow.payment_status = 'REFUNDED'
            borrow.save()

            # Sending return confirmation email.
            send_borrow_return_confirmation_email(user, 'Book return Successful', borrow, user.email, 'borrow_app/return_confirmation_email.html')

        return redirect(reverse_lazy('profile'))

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
