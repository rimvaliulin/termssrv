from django.contrib import admin
from .models import Book, Term


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    prepopulated_fields = {'short_name': ('name',)}
    list_display = ('name', 'short_name', 'version', 'pub_date')
    ordering = ('-pub_date',)


@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ('book', 'code', 'value')
