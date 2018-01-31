from django import forms
from django.contrib.auth.models import User
from .models import Shop


class LoginForm(forms.ModelForm):
	class Meta:
		model=User
		fields=['username','password']


class Join1Form(forms.ModelForm):
	class Meta:
		model=User
		fields=['username','password','email']


class Join2Form(forms.ModelForm):
	class Meta:
		model=Shop
		fields=['name','addr','phone','site']