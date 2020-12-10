from .models import Version, Term
from rest_framework import serializers


class BookSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='book.id')
    name = serializers.CharField(source='book.name')
    short_name = serializers.CharField(source='book.short_name')
    version = serializers.CharField(source='name')
    description = serializers.CharField(source='book.description')

    class Meta:
        model = Version
        fields = [
            'id',
            'name',
            'short_name',
            'description',
            'version',
            'pub_date',
        ]


class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Term
        fields = ['code', 'value']
