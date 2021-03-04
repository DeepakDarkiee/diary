from entry.models import Comment
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


# class ContactForm(forms.ModelForm):
#     class Meta:
#         model = Contact
#         fields = ('name', 'email', 'body')
