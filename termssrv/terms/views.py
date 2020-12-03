from django.core.exceptions import ValidationError
from rest_framework import serializers, status, viewsets
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
        """
        Get a list of reference books relevant on a given date.
        """
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
        # fallback if pagination is not set
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Get the terms of a given directory of the current version.
        """
        recent = self.get_queryset()
        recent = recent.filter(short_name=pk).order_by('-pub_date')[:1]
        queryset = Term.objects.filter(book=recent).order_by('code')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = TermSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        # fallback if pagination is not set
        serializer = TermSerializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, pk=None):
        """
        Validate the terms of a given reference book of the current version.

        Check values of the given codes for the terms in the book.
        """
        recent = self.get_queryset()
        recent = recent.filter(short_name=pk).order_by('-pub_date')[:1]
        queryset = Term.objects.filter(book=recent)
        serializer = TermSerializer(data=request.data, many=True)
        if serializer.is_valid():
            terms = {term['code']: term['value'] for term in serializer.data}
            object_list = queryset.filter(code__in=list(terms.keys()))
            if object_list:
                errors = []
                # validate values for the terms
                for obj in object_list:
                    if obj.code in terms and obj.value != terms[obj.code]:
                        errors.append(obj)
                if errors:
                    serializer = TermSerializer(errors, many=True)
                    return Response(
                        serializer.data, status=status.HTTP_400_BAD_REQUEST
                    )
                else:
                    return Response({'status': 'validated'})
            else:
                return Response(
                    {'status': 'not found'}, status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    @action(
        detail=True, url_path=r'(?P<version>[\w_]+)', methods=['get', 'put']
    )
    def get_and_validate_terms(self, request, pk=None, version=None):
        """
        Get terms and validate the term of reference book of specific version.
        """
        queryset = Term.objects.filter(
            book__short_name=pk, book__version=version
        )
        if request.method == 'GET':
            # get list of specifed terms
            queryset = queryset.order_by('code')
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = TermSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            # fallback if pagination is not set
            serializer = TermSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            # check value of the given code for the term in the book
            serializer = TermSerializer(data=request.data)
            if serializer.is_valid():
                code = serializer.data['code']
                value = serializer.data['value']
                try:
                    term = queryset.get(code=code)
                    if term.value == value:
                        return Response({'status': 'validated'})
                    else:
                        return Response(
                            {'status': 'not valid'},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                except Term.DoesNotExist:
                    return Response(
                        {'status': 'not found'},
                        status=status.HTTP_404_NOT_FOUND,
                    )
            else:
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
