from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Book, Term


class BookListFilter(admin.SimpleListFilter):
    title = _('Reference Books')
    parameter_name = 'short_name'

    def lookups(self, request, model_admin):
        queryset = Book.objects.all().distinct().order_by('name')
        return queryset.values_list('short_name', 'name')

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(book__short_name=self.value())
        return queryset


class VersionListFilter(admin.SimpleListFilter):
    title = _('version')
    parameter_name = 'version'

    def lookups(self, request, model_admin):
        if 'short_name' in request.GET:
            short_name = request.GET.get('short_name')
            queryset = Book.objects.filter(short_name=short_name)
            return queryset.values_list('version', 'version')

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(book__version=self.value())
        return queryset


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    date_hierarchy = 'pub_date'
    prepopulated_fields = {'short_name': ('name',)}
    list_display = ('name', 'short_name', 'version', 'pub_date')
    ordering = ('name', 'version')


@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ('book', 'code', 'value')

    def get_list_filter(self, request):
        list_filter = [BookListFilter]
        if 'short_name' in request.GET:
            return list_filter + [VersionListFilter]
        return list_filter
