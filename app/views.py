from django.conf import settings
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from ipware import get_client_ip

from app.forms import WhitelistAddForm
from app.models import WhitelistEntry, WhitelistSettings


class WhitelistMixin:
    """This mixin retrieves the whitelist entry for the request user."""
    entry = None  # type: WhitelistEntry
    ip = None

    def get_context_data(self, **kwargs):
        kwargs.update({
            'entry': self.entry,
            'ip': self.ip,
        })
        # noinspection PyUnresolvedReferences
        return super().get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        # Todo: check for IP spoofing
        client_ip, is_routable = get_client_ip(request)

        # Catch cases of non-routable addresses in production
        if not settings.DEBUG and not is_routable:
            raise RuntimeError("Client IP is non-routable: {}".format(client_ip))

        self.ip = client_ip
        try:
            self.entry = WhitelistEntry.objects.get(ip=client_ip)
        except WhitelistEntry.DoesNotExist:
            pass
        # noinspection PyUnresolvedReferences
        return super().dispatch(request, *args, **kwargs)


class IndexView(WhitelistMixin, TemplateView):
    template_name = 'whitelink/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'all_entries': WhitelistEntry.objects.all(),
            'whitelist_settings': WhitelistSettings.get(),
            'usage': settings.USAGE_INSTRUCTIONS,
        })
        return context

    def post(self, request, *args, **kwargs):
        """Adds entry to the whitelist."""
        if self.entry:
            # IP is already whitelisted
            raise PermissionDenied

        form = WhitelistAddForm(request.POST)

        if form.is_valid():
            # Set as admin if it's the first entry
            is_admin = WhitelistEntry.objects.count() == 0
            form.add(ip=self.ip, is_admin=is_admin)
            messages.success(request, "You can now access the server!")
            return redirect('index')

        # Re-render form on errors
        context = self.get_context_data(**kwargs)
        context.update({
            'form': form
        })
        return self.render_to_response(context)


class RevokeView(WhitelistMixin, View):
    """Revokes access of the entry."""

    def post(self, request, entry_id=None):
        # Check if whitelisted
        if self.entry is None:
            raise PermissionDenied

        if entry_id is None:
            # Revoke self
            self.entry.revoke()
        else:
            # Revoke other, need admin permission
            if not self.entry.is_admin:
                raise PermissionDenied
            obj = get_object_or_404(WhitelistEntry, pk=entry_id)
            obj.revoke()

        msg = "Your IP is removed from the whitelist." if entry_id is None else "User is removed from the whitelist."
        messages.info(request, msg)
        return redirect('index')
