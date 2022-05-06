from django import forms
from .models import Collection

class CreateCollectionModelForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = [
            'name',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter collection name'}),
        }