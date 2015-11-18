from django import forms

class SearchForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        required = True
    )

