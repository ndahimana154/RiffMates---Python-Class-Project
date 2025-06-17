from django import forms
from .models import Venue,Musician

VenueForm = forms.modelform_factory(Venue, fields=("name","description","picture"))


class MusicianForm(forms.ModelForm):
    class Meta:
        model = Musician
        fields = ['first_name', 'last_name', 'description', 'bio_pic', 'birth']
        widgets = {
            'birth': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }