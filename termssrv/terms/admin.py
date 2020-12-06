from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Book, Term


class TermsAdminSite(admin.AdminSite):
    site_header = _('Terminology Service')

    def each_context(self, request):
        context = super().each_context(request)
        # TODO: use distinct('name') for postgresql
        queryset = Book.objects.all().order_by('-pub_date')
        queryset = queryset.values_list('name', 'short_name', 'version')
        count = 0
        distinct = []
        for name, short_name, version in queryset:
            if name not in distinct:
                query = f'?short_name={short_name}&version={version}'
                context['available_apps'][1]['models'].insert(
                    count,
                    {
                        'add_url': '/admin/terms/term/add/',
                        'admin_url': '/admin/terms/term/' + query,
                        'name': name,
                        'object_name': 'Term',
                        'perms': {
                            'add': True,
                            'change': True,
                            'delete': True,
                            'view': True,
                        },
                    },
                )
                count += 1
                distinct.append(name)
        return context


site = TermsAdminSite(name='terms_admin_site')


class BookListFilter(admin.SimpleListFilter):
    title = _('Reference Books')
    parameter_name = 'short_name'

    def lookups(self, request, model_admin):
        queryset = Book.objects.all().distinct().order_by('name')
        return queryset.values_list('short_name', 'name')

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(book__short_name=self.value())


class VersionListFilter(admin.SimpleListFilter):
    title = _('version')
    parameter_name = 'version'

    def lookups(self, request, model_admin):
        short_name = request.GET['short_name']
        queryset = Book.objects.filter(short_name=short_name)
        return queryset.values_list('version', 'version')

    def queryset(self, request, queryset):
        if self.value():
            short_name = request.GET.get('short_name', None)
            is_exists = Book.objects.filter(
                short_name=short_name, version=self.value()
            ).count()
            if is_exists:
                return queryset.filter(book__version=self.value())
            return queryset


@admin.register(Book, site=site)
class BookAdmin(admin.ModelAdmin):
    date_hierarchy = 'pub_date'
    prepopulated_fields = {'short_name': ('name',)}
    list_display = ('name', 'short_name', 'version', 'pub_date')
    ordering = ('name', 'version')


@admin.register(Term, site=site)
class TermAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        if 'short_name' in request.GET:
            return ('code', 'value')
        return ('book', 'code', 'value')

    def get_list_filter(self, request):
        if 'short_name' in request.GET:
            return (BookListFilter, VersionListFilter)
        return (BookListFilter,)


from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin

site.register(User, UserAdmin)
site.register(Group, GroupAdmin)
