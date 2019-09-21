from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

from .models import ViewsMovie, Movie
from .filters import SelectedUsersFilter
from .serializers import SimpleSqlSerializer
from rg_test.utilites.matrix import matrix_load_from_cache


class SimpleSqlView(ListAPIView):
    """
    sql recommendation
    """
    serializer_class = SimpleSqlSerializer
    filterset_class = SelectedUsersFilter
    queryset = ViewsMovie.objects.values_list('movie_id', flat=True)


class CollaborativeView(APIView):
    """
    Collaborative recommendation
    """

    def get(self, request, *args, **kwargs):
        from scipy.sparse import lil_matrix
        import numpy as np
        import time
        start_time = time.time()

        coll_matrix = matrix_load_from_cache('recommendation_matrix')

        # подготавливаем вектор просмотров пользователя:

        user_id = request.query_params.get('user_id')
        assert user_id, \
            "Не задан номер пользователя!"

        user_vector = lil_matrix((coll_matrix.shape[-1], 1))
        for movie_id in ViewsMovie.objects.filter(user_id=user_id).values_list('movie_id', flat=True):
            user_vector[movie_id, 0] = 1
        user_vector = user_vector.tocsr()

        # перемножить матрицу item-item и вектор просотров пользователя
        x = coll_matrix.dot(user_vector).tolil()
        # занулить ячейки, соответствующие фильмам, которые пользователь уже посмотрел
        for i, j in zip(*user_vector.nonzero()):
            x[i, j] = 0
        # превращаем столбец результата в вектор
        x = x.T.tocsr()
        # отсортировать фильмы в порядке убывания значений и получить top-k рекомендаций (quorum = 100)
        quorum = 100
        data_ids = np.argsort(x.data)[-quorum:][::-1]

        data = []
        for arg_id in data_ids:
            row_id, weight = x.indices[arg_id], x.data[arg_id]
            data.append({"movie_id": row_id, "weight": weight})
        return Response({'compilation_time': (time.time() - start_time), "results": data})
