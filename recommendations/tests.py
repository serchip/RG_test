from django.core.management import call_command

from rg_test.tests.test_case import CRMAPIClientTestCase
from rg_test.tests.factories import UserFactory
from recommendations.factories import MoviesFactory, ViewsMovieFactory


class RecommendationsTestMixin(CRMAPIClientTestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = UserFactory.create()
        user2 = UserFactory.create()
        user3 = UserFactory.create()
        user4 = UserFactory.create()
        user5 = UserFactory.create()

        for _ in range(10):
            MoviesFactory.create()

        ViewsMovieFactory.create(user=user1, movie_id=1)
        ViewsMovieFactory.create(user=user1, movie_id=2)
        ViewsMovieFactory.create(user=user1, movie_id=3)
        ViewsMovieFactory.create(user=user2, movie_id=3)
        ViewsMovieFactory.create(user=user2, movie_id=4)
        ViewsMovieFactory.create(user=user3, movie_id=4)
        ViewsMovieFactory.create(user=user4, movie_id=5)
        ViewsMovieFactory.create(user=user4, movie_id=6)
        ViewsMovieFactory.create(user=user5, movie_id=6)

    def simple_test(self, url_name):

        response = self.get(url_name, query_params={'user_id': 1})
        self.assertEqual(response.status_code, 200)
        movie_id = 4
        self.assertIn(movie_id, [i['movie_id'] for i in response.data['results']])
        movie_id = 5
        self.assertNotIn(movie_id, [i['movie_id'] for i in response.data['results']])

        response = self.get(url_name, query_params={'user_id': 2})
        self.assertEqual(response.status_code, 200)
        movie_id = 1
        self.assertIn(movie_id, [i['movie_id'] for i in response.data['results']])
        movie_id = 2
        self.assertIn(movie_id, [i['movie_id'] for i in response.data['results']])
        movie_id = 5
        self.assertNotIn(movie_id, [i['movie_id'] for i in response.data['results']])

        response = self.get(url_name, query_params={'user_id': 3})
        self.assertEqual(response.status_code, 200)
        self.assertEqual([3], [i['movie_id'] for i in response.data['results']])

        response = self.get(url_name, query_params={'user_id': 4})
        self.assertEqual(response.status_code, 200)
        self.assertEqual([], [i['movie_id'] for i in response.data['results']])

        response = self.get(url_name, query_params={'user_id': 5})
        self.assertEqual(response.status_code, 200)
        self.assertEqual([5], [i['movie_id'] for i in response.data['results']])

    def test_simple_sql(self):
        self.simple_test('simple_sql')

    def test_collaborative_method(self):
        call_command('compile_collaborative_matrix')
        self.simple_test('collaborative')
