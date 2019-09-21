from django.db import models
from django.contrib.postgres.indexes import BrinIndex
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class Movie(models.Model):
    name = models.CharField(verbose_name=_('Название фильма'), max_length=255)


class ViewsMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=False)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, db_index=False)
    count_view = models.PositiveSmallIntegerField(verbose_name=_('Кол-во просмотров'), default=1)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['user', 'movie']]
        indexes = (
            BrinIndex(fields=['timestamp']),
        )
