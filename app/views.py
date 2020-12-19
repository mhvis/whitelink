from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.views.generic import TemplateView
from ipware import get_client_ip

from app.forms import WhitelistForm
from app.models import WhitelistEntry


class WhitelistMixin:
    """This mixin retrieves the whitelist entry for the request user."""
    entry = None
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
        })
        return context

    def post(self, request, *args, **kwargs):
        """This validates the whitelist add form."""
        if self.entry:
            raise PermissionDenied

        form = WhitelistForm(request.POST)

        if form.is_valid():
            WhitelistEntry.objects.create(ip=self.ip,
                                          friendly_name=form.cleaned_data.get('name'),
                                          is_admin=True)
            return redirect('index')

        context = self.get_context_data(**kwargs)
        context.update({
            'form': form
        })
        return self.render_to_response(context)
