from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError


class WhitelistForm(forms.Form):
    code = forms.CharField(max_length=100)
    name = forms.CharField(max_length=100)

    def clean(self):
        code = self.cleaned_data.get('code')

        if code != settings.ACCESS_CODE:
            raise ValidationError("Access code is invalid.")

        return self.cleaned_data