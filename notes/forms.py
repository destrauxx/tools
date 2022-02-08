from django import forms

from .models import Note, Collection

class CreateNoteModelForm(forms.ModelForm):

    class Meta:
        model = Note
        fields = [
            'header',
            'text',
        ]
        widgets = {
            'header': forms.TextInput(attrs={'placeholder': 'Note header'}),
        }

class CreateCollectionModelForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = [
            'name',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter collection name'}),
        }