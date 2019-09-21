from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Recalculate cosine distance between users'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        from sklearn.preprocessing import normalize
        from scipy.sparse import spdiags
        from scipy.sparse import lil_matrix

        from recommendations.models import Movie, ViewsMovie
        from rg_test.utilites.matrix import matrix_save_to_cache, matrix_load_from_cache

        len_row = Movie.objects.latest('id').id + 1
        len_col = User.objects.latest('id').id + 1
        matrix = lil_matrix((len_row, len_col))
        # заполняем матрицу
        for obj_id, user_id, view in ViewsMovie.objects.values_list('movie_id', 'user_id', 'count_view'):
            row_id = obj_id
            col_id = user_id
            if row_id is not None and col_id is not None:
                matrix[row_id, col_id] = max(view, 0)

        # косинусная мера вычисляется как отношение скалярного произведения векторов(числитель)
        # к произведению длины векторов(знаменатель)
        # нормализуем исходную матрицу
        normalized_matrix = normalize(matrix.tocsr()).tocsr()
        # вычисляем скалярное произведение
        cosine_sim_matrix = normalized_matrix.dot(normalized_matrix.T)
        # обнуляем диагональ, чтобы исключить просмотренные объекты
        diag = spdiags(-cosine_sim_matrix.diagonal(), [0], *cosine_sim_matrix.shape, format='csr')
        cosine_sim_matrix = cosine_sim_matrix + diag

        matrix_save_to_cache(cosine_sim_matrix, 'recommendation_matrix')

        self.stdout.write(self.style.SUCCESS('Successfully Recalculate data '))
