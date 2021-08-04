from django import forms
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _
from bootstrap_modal_forms.forms import BSModalModelForm

from .models import Note


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'body']

        error_messages = {
            'title': {'unique': _('This title is not allowed, please choose a new one.')}
        }

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['slug'] = slugify(cleaned_data['title'])

        return cleaned_data

"""
class NoteForm(BSModalModelForm):
    class Meta:
        model = Note
        fields = ['title', 'body']

        error_messages = {
            'title': {'unique': _('This title is not allowed, please choose a new one.')}
        }

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['slug'] = slugify(cleaned_data['title'])

        return cleaned_data
"""
