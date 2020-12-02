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
    version = models.CharField(_('version'), max_length=30)
    pub_date = models.DateField(_('date'), auto_now_add=True)

    class Meta:
        verbose_name = _('Reference Book')
        verbose_name_plural = _('Reference Books')
        constraints = [
            models.UniqueConstraint(
                fields=['short_name', 'name', 'version'],
                name='unique_book_version',
            ),
            models.UniqueConstraint(
                fields=['name', 'version'],
                name='unique_book_name_per_version',
            ),
            models.UniqueConstraint(
                fields=['short_name', 'version'],
                name='unique_book_short_name_per_version',
            ),
        ]

    def __str__(self):
        return f'{self.short_name} ({self.version})'
