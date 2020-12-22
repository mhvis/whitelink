from django import forms
from django.core.exceptions import ValidationError

from app.models import WhitelistSettings, WhitelistEntry


class WhitelistAddForm(forms.Form):
    """Form for adding a new entry into the whitelist."""
    code = forms.CharField(max_length=100)
    name = forms.CharField(max_length=100)

    def clean(self):
        wl_settings = WhitelistSettings.get()

        # Check access code
        code = self.cleaned_data.get('code')

        if code != wl_settings.code:
            raise ValidationError("Access code is invalid.")

        # Check capacity
        if WhitelistEntry.objects.count() >= wl_settings.max_entries:
            raise ValidationError("Whitelist is full, ask the host to increase the number of allowed entries.")

        return self.cleaned_data

    def add(self, ip: str, is_admin: bool):
        """Adds entry to the whitelist."""
        WhitelistEntry.objects.add(ip=ip,
                                   friendly_name=self.cleaned_data.get('name'),
                                   is_admin=is_admin)
