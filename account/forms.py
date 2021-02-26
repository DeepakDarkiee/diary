from django import forms
from django.contrib.auth.models import User

class PasswordChangeForm(forms.Form):
	old_password = forms.CharField(widget=forms.PasswordInput)
	new_password = forms.CharField(widget=forms.PasswordInput)
	confirm_password = forms.CharField(widget=forms.PasswordInput)



# class ProfileForm(forms.ModelForm):

#     class Meta:
#         model = User
#         fields = "__all__"  