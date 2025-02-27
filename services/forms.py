from django import forms


class SearchForm(forms.Form):
    title = forms.CharField(max_length=100)


class PaymentForm(forms.Form):
    card_number = forms.CharField(max_length=16, min_length=16)
    expiry_date = forms.CharField(max_length=5)
    cvv = forms.CharField(max_length=3, min_length=3)
