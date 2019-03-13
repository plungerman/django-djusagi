from django import forms


class SearchForm(forms.Form):
    username = forms.CharField(
        label="Username",
        required = False
    )
    phile = forms.FileField(
        label="Upload CSV file",
        required = False,
        help_text="First column must be username or email address"
    )

