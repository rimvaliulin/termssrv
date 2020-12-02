from django.core.exceptions import ValidationError
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Book, Term
from .serializers import BookSerializer, TermSerializer


class BookViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows books to be viewed
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @action(
        detail=False,
        url_path=r'(?P<date>[0-9]{4}-[0-9]{2}-[0-9]{2})'
    )
    def recent_books(self, request, date=None):
        """получение списка справочников, актуальных на указанную дату"""
        queryset = self.get_queryset().order_by('-pub_date')
        try:
            queryset = self.queryset.filter(pub_date__gte=date)
        except ValidationError as e:
            raise serializers.ValidationError(detail=e.messages)
        else:
            page = self.paginate_queryset(queryset)
            serializer = self.get_serializer(page or queryset, many=True)
            return Response(serializer.data)

    @action(detail=True, url_path=r'terms')
    def current_terms(self, request, pk=None):
        return Response([])

    @action(detail=True, url_path=r'terms', methods=['post'])
    def validate_current_terms(self, request, pk=None):
        return Response([])

    @action(detail=True, url_path=r'terms/<str:version>/')
    def terms_by_version(self, request, pk=None):
        return Response([])

    @action(detail=True, url_path=r'terms/<str:version>/', methods=['post'])
    def validate_term_by_version(self, request, pk=None):
        return Response([])
