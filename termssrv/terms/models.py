from django.db import models
from django.utils.translation import gettext_lazy as _


class Book(models.Model):
    """
    The reference book of terms.

    The version of the reference book must be unique
    within that reference book.

    Name, short name are required.
    Description is optional.
    """

    name = models.CharField(_('name'), max_length=150)
    short_name = models.CharField(_('short name'), max_length=50)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        verbose_name = _('Reference Book')
        verbose_name_plural = _('Reference Books')
        constraints = [
            models.UniqueConstraint(
                fields=['short_name', 'name'],
                name='unique_names',
            ),
        ]

    def __str__(self):
        return self.name


class Version(models.Model):
    """
    THe version of the reference book.

    Name and publication data are requied.
    """

    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, verbose_name=_('version')
    )
    name = models.CharField(_('name'), max_length=50)
    pub_date = models.DateField(_('date'))

    def __str__(self):
        return f'{self.book} ({self.name})'

    class Meta:
        verbose_name = _('Version')
        verbose_name_plural = _('Versions')
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'book'],
                name='unique_version_name',
            ),
        ]


class Term(models.Model):
    """
    The element of the reference book.

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
                name='unique_term_per_version',
            ),
        ]

    def __str__(self):
        return f'{self.code} ({self.version})'
