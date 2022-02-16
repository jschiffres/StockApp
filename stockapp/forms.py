from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from .models import Portfolio, Transaction, Holding

class CreateUserForm(UserCreationForm):
	email = forms.EmailField(required=True)
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

class CreatePortfolioForm(ModelForm):
	class Meta:
		model = Portfolio
		fields = ['title', 'value']

class EditPortfolioForm(ModelForm):
	class Meta:
		model = Portfolio
		fields = ['title']

class BuyForm(ModelForm):
	class Meta:
		model = Holding
		fields = ['shares','portfolio']

class SellForm(ModelForm):
	class Meta:
		model = Holding
		fields = ['ticker','shares']