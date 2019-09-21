import factory

from rg_test.tests.factories import UserFactory
from .models import Movie, ViewsMovie


class MoviesFactory(factory.DjangoModelFactory):
    class Meta:
        model = Movie
    name = factory.Sequence(lambda n: 'Movie %d' % n)


class ViewsMovieFactory(factory.DjangoModelFactory):
    class Meta:
        model = ViewsMovie

    user = factory.SubFactory(UserFactory)
    movie = factory.SubFactory(MoviesFactory)
