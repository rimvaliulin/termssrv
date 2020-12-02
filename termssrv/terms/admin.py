from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    prepopulated_fields = {"short_name": ("name",)}
    list_display = ('name', 'short_name', 'version', 'date_added')
    ordering = ('-date_added',)
