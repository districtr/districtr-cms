from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ClientConfig(AppConfig):
    name = "districtrcms.client"
    verbose_name = _("Client")

    def ready(self):
        try:
            import districtrcms.client.signals  # noqa F401
        except ImportError:
            pass
