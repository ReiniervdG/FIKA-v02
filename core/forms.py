from django import forms

from .models import Provider


class ProviderChoiceForm(forms.Form):
    provider = forms.ModelChoiceField(queryset=Provider.objects.all())
