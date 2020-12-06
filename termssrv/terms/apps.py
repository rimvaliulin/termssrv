from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig
from django.utils.translation import gettext_lazy as _


class TermsConfig(AppConfig):
    name = 'termssrv.terms'
    verbose_name = _('Terminology service')


class TermsAdminConfig(AdminConfig):
    default_site = 'termssrv.terms.admin.TermsAdminSite'
