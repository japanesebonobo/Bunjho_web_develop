from django import forms
from .models import GENERATION_CHOICES
from .models import GENRE_CHOICES

class SearchForm(forms.Form):
    faculty = forms.ChoiceField(label='課程', choices=GENERATION_CHOICES, required=False)
    genre = forms.ChoiceField(label='科目ジャンル', choices=GENRE_CHOICES, required=False)

SearchFormSet = forms.formset_factory(SearchForm, extra=1)