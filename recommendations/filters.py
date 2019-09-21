from django_filters import FilterSet
from django.db.models import Count

from recommendations.models import ViewsMovie


class SelectedUsersFilter(FilterSet):
    def filter_queryset(self, queryset):
        user_id = self.request.query_params.get('user_id')
        assert user_id, \
            "Не задан номер пользователя!"

        user_view_movie = queryset.filter(user_id=user_id)
        queryset = ViewsMovie.objects.filter(user_id__in=ViewsMovie.objects.filter(
                                        movie_id__in=user_view_movie
                                        ).values_list('user_id', flat=True)
                                  ).exclude(movie_id__in=user_view_movie).values('movie_id')\
                                  .annotate(Count('movie_id')).order_by('-movie_id__count')
        return queryset
