from django import forms
from django.core.exceptions import ValidationError

from app.models import WhitelistSettings


class WhitelistAddForm(forms.Form):
    code = forms.CharField(max_length=100)
    name = forms.CharField(max_length=100)

    def clean(self):
        code = self.cleaned_data.get('code')

        if code != WhitelistSettings.get().code:
            raise ValidationError("Access code is invalid.")

        return self.cleaned_data
