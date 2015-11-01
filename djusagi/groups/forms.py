from django import forms

class SearchForm(forms.Form):
    email = forms.CharField(
        label="Email",
        required = True
    )

