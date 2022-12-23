from django import forms


class SearchForm(forms.Form):
    query = forms.CharField(label='جستجو', max_length=100)
    catid = forms.IntegerField()


