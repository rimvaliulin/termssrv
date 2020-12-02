from .models import Book, Term
from rest_framework import serializers


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('name', 'short_name', 'description', 'version', 'pub_date')


class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Term
        fields = ('book', 'code', 'value')
