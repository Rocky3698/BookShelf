from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .constants import GENDER_TYPE
from .models import UserAddress,Account


class SignUpForm(UserCreationForm):
    birth_date = forms.DateField(label='',widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Birth Date'}))
    gender = forms.ChoiceField(choices=GENDER_TYPE,label='',widget=forms.Select(attrs={'placeholder': 'Gender'}))
    street_address = forms.CharField(max_length=100,label='',widget=forms.TextInput(attrs={'placeholder': 'Street Address'}))
    city = forms.CharField(max_length=100,label='',widget=forms.TextInput(attrs={'placeholder': 'City'}))
    postal_code = forms.IntegerField(label='',widget=forms.NumberInput(attrs={'placeholder': 'Postal Code'}))
    country = forms.CharField(max_length=100,label='',widget=forms.TextInput(attrs={'placeholder': 'Country'}))
    password1=forms.CharField(label='',widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
    password2=forms.CharField(label='',widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password'}))
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'birth_date','gender', 'postal_code', 'city','country', 'street_address']
        
        widgets={
            'first_name':forms.TextInput(attrs={'placeholder':'First name'}),
            'last_name':forms.TextInput(attrs={'placeholder':'Last name'}),
            'email':forms.TextInput(attrs={'placeholder':'Email'}),
            'username':forms.TextInput(attrs={'placeholder':'Username'}),
        }
        labels={
            'first_name':'',
            'last_name':'',
            'email':'',
            'username':'',
        }

        help_texts = {
            'username': None,
        }
    def save(self, commit=True):
        our_user = super().save(commit=False) 
        if commit == True:
            our_user.save()
            gender = self.cleaned_data.get('gender')
            postal_code = self.cleaned_data.get('postal_code')
            country = self.cleaned_data.get('country')
            birth_date = self.cleaned_data.get('birth_date')
            city = self.cleaned_data.get('city')
            street_address = self.cleaned_data.get('street_address')

            UserAddress.objects.create(
                user = our_user,
                postal_code = postal_code,
                country = country,
                city = city,
                street_address = street_address
            )
            Account.objects.create(
                user = our_user,
                gender = gender,
                birth_date =birth_date,
            )
        return our_user


class ProfileForm(forms.ModelForm):
    birth_date = forms.DateField(label='',widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Birth Date'}))
    gender = forms.ChoiceField(choices=GENDER_TYPE,label='',widget=forms.Select(attrs={'placeholder': 'Gender'}))
    street_address = forms.CharField(max_length=100,label='',widget=forms.TextInput(attrs={'placeholder': 'Street Address'}))
    city = forms.CharField(max_length=100,label='',widget=forms.TextInput(attrs={'placeholder': 'City'}))
    postal_code = forms.IntegerField(label='',widget=forms.NumberInput(attrs={'placeholder': 'Postal Code'}))
    country = forms.CharField(max_length=100,label='',widget=forms.TextInput(attrs={'placeholder': 'Country'}))
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets={
            'first_name':forms.TextInput(attrs={'placeholder':'First name'}),
            'last_name':forms.TextInput(attrs={'placeholder':'Last name'}),
            'email':forms.TextInput(attrs={'placeholder':'Email'}),
        }
        labels={
            'first_name':'',
            'last_name':'',
            'email':'',
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.instance:
            try:
                user_account = self.instance.account
                user_address = self.instance.address
            except Account.DoesNotExist:
                user_account = None
                user_address = None

            if user_account:
                self.fields['gender'].initial = user_account.gender
                self.fields['birth_date'].initial = user_account.birth_date
                self.fields['street_address'].initial = user_address.street_address
                self.fields['city'].initial = user_address.city
                self.fields['postal_code'].initial = user_address.postal_code
                self.fields['country'].initial = user_address.country

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            user_account, created = Account.objects.get_or_create(user=user)
            user_address, created = UserAddress.objects.get_or_create(user=user) 

            user_account.gender = self.cleaned_data['gender']
            user_account.birth_date = self.cleaned_data['birth_date']
            user_account.save()

            user_address.street_address = self.cleaned_data['street_address']
            user_address.city = self.cleaned_data['city']
            user_address.postal_code = self.cleaned_data['postal_code']
            user_address.country = self.cleaned_data['country']
            user_address.save()

        return user
    

class DepositeForm(forms.Form):
    amount = forms.DecimalField(label='amount', max_digits=12, decimal_places=2)
    def clean_amount(self): # amount field ke filter korbo
        min_deposit_amount = 10
        amount = self.cleaned_data.get('amount') # user er fill up kora form theke amra amount field er value ke niye aslam, 50
        if amount < min_deposit_amount:
            raise forms.ValidationError(
                f'You need to deposit at least {min_deposit_amount} $'
            )

        return amount