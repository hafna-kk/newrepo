from django.forms import ModelForm, Textarea
from .models import Review
from .models import Movie
from django import forms

class ReviewForm(ModelForm):
    """form for the reivew page."""

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['watch_again'].widget.attrs.update({
            'class': 'form-check-input'
        })

    class Meta:
        model = Review

        fields = ['text', 'watch_again']
        labels = {
            'watch_again': ('Watch Again')
        }
        widgets = {
            'text': Textarea(attrs={'rows': 4}),
        }
class MovieForm(forms.ModelForm):
    class Meta:
        model=Movie
        fields = ['title','description','image','category','year','release_date','actors','url']
