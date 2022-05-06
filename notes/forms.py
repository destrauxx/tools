from django import forms

from .models import Note

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
