from django import forms
from django_summernote.widgets import SummernoteInplaceWidget,SummernoteWidget

class AddForm(forms.Form):

    productivity = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'type': 'range',
                'min': '0',
                'max': '10',
                'value': '5',
                'step': '1',
                'class': 'mb-3 form-control'
            }
        ),
        label='Rate Today\'s Productivity',
        required=True
    )

    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Name this day (anything you like)',
                'class': " form-control mb-3",
            }
        ),
        label='',
        required=True
    )

    content = forms.CharField(
        widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '600px'}}))
    
