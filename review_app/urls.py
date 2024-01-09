from django.urls import path
from django.contrib.auth import views as auth_views
from .views import SignUp_Form_View, SignIn_View, SignOut_View, Profile_View, ProfileEdit_View, PasswordChange_View, RechargeWallet_View

urlpatterns = [
    path('user/signup/',        SignUp_Form_View.as_view(),     name='signup'),
    path('user/signin/',        SignIn_View.as_view(),          name='signin'),
    path('user/signout/',       SignOut_View.as_view(),         name='signout'),

    path('user/profile/',           Profile_View.as_view(),         name='profile'),
    path('user/profile_edit/',      ProfileEdit_View.as_view(),     name='profile_edit'),
    path('user/password_change/',   PasswordChange_View.as_view(),  name='password_change'),
    path('user/recharge_wallet/',   RechargeWallet_View.as_view(),  name='recharge_wallet'),

    path('password_reset/',                    auth_views.PasswordResetView.as_view(template_name='user_app/password_reset_form.html'),                name='password_reset'),
    path('password_reset/done/',               auth_views.PasswordResetDoneView.as_view(template_name='user_app/password_reset_done.html'),            name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/',   auth_views.PasswordResetConfirmView.as_view(template_name='user_app/password_reset_confirm.html'),      name='password_reset_confirm'),
    path('password_reset/complete/',           auth_views.PasswordResetCompleteView.as_view(template_name='user_app/password_reset_complete.html'),    name='password_reset_complete'),
]
