from rest_framework import serializers

from .models import ViewsMovie


class SimpleSqlSerializer(serializers.ModelSerializer):
    m_count = serializers.IntegerField(
        source='movie_id__count'
    )

    class Meta:
        model = ViewsMovie
        fields = ('movie_id', 'm_count')
