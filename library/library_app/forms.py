from django import forms

# My forms

class BookQueryForm(forms.Form):
    query = forms.CharField(label="Search: ", max_length=100)