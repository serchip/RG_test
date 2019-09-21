from django.core.cache import cache
TIME_OUT = 3000


def matrix_save_to_cache(matrix, key):
    coo_m = matrix.tocoo()
    cache.set('{0}:data'.format(key), coo_m.data.tolist(), TIME_OUT)
    cache.set('{0}:row'.format(key), coo_m.row.tolist(), TIME_OUT)
    cache.set('{0}:col'.format(key), coo_m.col.tolist(), TIME_OUT)
    return True


def matrix_load_from_cache(key):
    import numpy as np
    from scipy.sparse import csr_matrix

    row = np.array(cache.get('{0}:row'.format(key)))
    col = np.array(cache.get('{0}:col'.format(key)))
    data = np.array(cache.get('{0}:data'.format(key)))
    assert data.any(), \
        "Не найдена матрица по key={0}".format(key)

    return csr_matrix((data, (row, col)))
