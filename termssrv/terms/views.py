from django.core.exceptions import ValidationError
from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Book, Term
from .serializers import BookSerializer, TermSerializer


class BookViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows books and terms to be viewed and validated.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @action(detail=False, url_path=r'(?P<date>[0-9]{4}-[0-9]{2}-[0-9]{2})')
    def recent_books(self, request, date=None):
        """Get a list of reference books relevant on a given date"""
        queryset = self.get_queryset()
        try:
            queryset = self.queryset.filter(pub_date__gte=date)
        except ValidationError as e:
            raise serializers.ValidationError(detail=e.messages)
        queryset = queryset.order_by('-pub_date')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Get the elements of a given directory of the current version"""
        recent = self.get_queryset()
        recent = recent.filter(short_name=pk).order_by('-pub_date')[:1]
        queryset = Term.objects.filter(book=recent).order_by('code')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = TermSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = TermSerializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, pk=None):
        return Response([])

    @action(detail=True, url_path=r'(?P<version>[\w_]+)')
    def terms_by_version(self, request, pk=None, version=None):
        """Get the elements of a given reference book of the specified version"""
        queryset = Term.objects.filter(
            book__short_name=pk, book__version=version
        ).order_by('code')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = TermSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = TermSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, url_path=r'(?P<version>[\w_]+)', methods=['post'])
    def validate_term_by_version(self, request, pk=None):
        return Response([])
