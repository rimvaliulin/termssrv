from .models import Book, Version, Term
from rest_framework import serializers


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'id',
            'name',
            'short_name',
            'description',
        ]


class VersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Version
        fields = [
            'id',
            'name',
            'pub_date',
        ]


class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Term
        fields = ['code', 'value']
