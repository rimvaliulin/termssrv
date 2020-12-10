from django.db import models
from django.utils.translation import gettext_lazy as _


class Book(models.Model):
    """
    The reference book of terms.

    The version of the reference book must be unique
    within that reference book.

    Name, short name and publication date are required.
    Description is optional.
    """

    name = models.CharField(_('name'), max_length=150)
    short_name = models.CharField(_('short name'), max_length=50)
    description = models.TextField(_('description'), blank=True)
    pub_date = models.DateField(_('date'))

    class Meta:
        verbose_name = _('Reference Book')
        verbose_name_plural = _('Reference Books')
        constraints = [
            models.UniqueConstraint(
                fields=['short_name', 'name'],
                name='unique_book_version',
            ),
        ]

    def __str__(self):
        return f'{self.short_name} ({self.version})'


class Version(models.Model):
    """
    A version of the reference book.

    Name is requied.
    """

    name = models.CharField(_('name'), max_length=50)
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, verbose_name=_('version')
    )

    def __str__(self):
        return f'{self.name} ({self.book_id})'


class Term(models.Model):
    """
    An element of the reference book.

    Code and value are required.
    """

    version = models.ForeignKey(
        Version, on_delete=models.CASCADE, verbose_name=_('version')
    )
    code = models.CharField(_('code'), max_length=50)
    value = models.CharField(_('value'), max_length=100)

    class Meta:
        verbose_name = _('Term')
        verbose_name_plural = _('Terms')
        constraints = [
            models.UniqueConstraint(
                fields=['code', 'version'],
                name='unique_terms_per_book',
            ),
        ]

    def __str__(self):
        return f'{self.code} ({self.version_id})'
