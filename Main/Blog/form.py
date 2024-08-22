from django import forms
from froala_editor.widgets import FroalaEditor  # Corrected to froala_editor
from .models import *

class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogModel
        fields = [ 'content']
        widgets = {
            'content': FroalaEditor(),  # Use FroalaEditor for the 'content' field
        }
