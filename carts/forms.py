from django import forms

class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Password',
        'class': 'input-group',
    }))