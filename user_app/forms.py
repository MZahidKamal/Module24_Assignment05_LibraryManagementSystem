from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

from .models import UserAddress, UserProfile

class SignUp_Form(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    road_and_house = forms.CharField(max_length=500, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    zip_code = forms.IntegerField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    state = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    country = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'road_and_house',
            'zip_code',
            'city',
            'state',
            'country',
            'email',
            'username',
            'password1',
            'password2',
        )

    def save(self, commit=True):
        new_user = super(SignUp_Form, self).save(commit=False)
        if commit:
            new_user.save()
            new_address = UserAddress.objects.create(
                user=new_user,
                road_and_house=self.cleaned_data.get('road_and_house'),
                zip_code=self.cleaned_data.get('zip_code'),
                city=self.cleaned_data.get('city'),
                state=self.cleaned_data.get('state'),
                country=self.cleaned_data.get('country'),
            )
            UserProfile.objects.create(
                user=new_user,
                user_address=new_address,
                wallet_balance=100,                                         # 100 € is added as SignUp Bonus
            )
            return new_user

    def __init__(self, *args, **kwargs):
        super(SignUp_Form, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class UserEdit_Form(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
        )

    def __init__(self, *args, **kwargs):
        super(UserEdit_Form, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class UserAddressEdit_Form(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = (
            'road_and_house',
            'zip_code',
            'city',
            'state',
            'country',
        )

    def __init__(self, *args, **kwargs):
        super(UserAddressEdit_Form, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""
The approach used to create the signup form is an advance approach. It combines all the fields of all models, show a single
form to the user, collect all information, and then create separate instances for separate models, and then save them into
the database.

But the approach used to create the profile edit form is comparatively the easier one. It keeps separate the fields of each
models, create separate forms, but in the views.py file it show a single form to the user, then collect all information,
and then create separate instances for separate models, and then save them into the database.
"""
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class UserWalletRecharge_Form(forms.Form):
    amount = forms.DecimalField(max_digits=8, decimal_places=2, min_value=5)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
