# IMPORT SECTION
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from django.views.generic.edit import CreateView, FormView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string

from .forms import SignUp_Form, UserEdit_Form, UserAddressEdit_Form, UserWalletRecharge_Form
from .models import UserProfile
from borrow_app.models import Borrow

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CREATE VIEWS SECTION

def send_recharge_confirmation_email(user, subject, amount, target_email, template_name):
    email_subject = subject
    message = render_to_string(template_name, {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'amount': amount,
        'wallet_balance': user.userprofile.wallet_balance,
    })
    to_email = target_email
    send_email = EmailMultiAlternatives(email_subject, '', to=[to_email])
    send_email.attach_alternative(message, 'text/html')
    send_email.send()

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class SignUp_Form_View(CreateView):
    form_class = SignUp_Form
    template_name = 'user_app/user_signup.html'
    success_url = reverse_lazy('signin')

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class SignIn_View(LoginView):
    form_class = AuthenticationForm
    template_name = 'user_app/user_signin.html'

    # If the user is already signed in, then the user can't visit the signin url, rather user will be redirected to profile.
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('profile')
        return super().dispatch(request, *args, **kwargs)

    # After successful login user will be redirected to profile.
    def get_success_url(self):
        success_url = reverse_lazy('profile')
        return success_url

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class SignOut_View(LoginRequiredMixin, View):

    # Signout url can only be visited if the user is authenticated and already signed in.
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
        return HttpResponseRedirect(reverse_lazy('signin'))

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class ProfileEdit_View(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_form = UserEdit_Form(instance=request.user)
        address_form = UserAddressEdit_Form(instance=request.user.useraddress)
        return render(request, 'user_app/user_profile_edit.html', {
            'user_form': user_form,
            'address_form': address_form
        })

    def post(self, request, *args, **kwargs):
        user_form = UserEdit_Form(request.POST, instance=request.user)
        address_form = UserAddressEdit_Form(request.POST, instance=request.user.useraddress)
        if user_form.is_valid() and address_form.is_valid():
            user_form.save()
            address_form.save()
            return HttpResponseRedirect(reverse_lazy('profile'))
        else:
            return render(request, 'user_app/user_profile_edit.html', {
                'user_form': user_form,
                'address_form': address_form
            })

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class PasswordChange_View(LoginRequiredMixin, PasswordChangeView):
    template_name = 'user_app/password_change.html'
    success_url = reverse_lazy('signin')

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Profile_View(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_borrows = Borrow.objects.filter(user_profile=self.request.user.userprofile).order_by('-id')
        context = {
            'user': request.user,
            'user_address': request.user.useraddress,
            'user_profile': request.user.userprofile,
            'user_borrows': user_borrows,
        }
        return render(request, 'user_app/user_profile.html', context)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class RechargeWallet_View(LoginRequiredMixin, FormView):
    form_class = UserWalletRecharge_Form
    template_name = 'user_app/recharge_wallet.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        user = self.request.user
        user_profile = UserProfile.objects.get(user=user)

        # User wallet is updating
        user_profile.wallet_balance += amount
        user_profile.save()

        # Sending confirmation email.
        send_recharge_confirmation_email(user, 'Wallet Recharge Successful', amount, user.email, 'user_app/wallet_recharge_confirmation_email.html')

        return super().form_valid(form)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
