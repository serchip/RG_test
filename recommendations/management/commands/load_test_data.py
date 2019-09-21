import random

from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = 'load test data to db'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        from django.contrib.auth.models import User
        from recommendations.models import Movie, ViewsMovie
        from rg_test.utilites.namegenerator import generate_word

        # --Insert User--
        batch_size = 10000 - User.objects.count()
        if batch_size > 0:
            objs = (User(username=generate_word(random.randint(10,20))) for _ in range(batch_size))
            User.objects.bulk_create(objs, batch_size)

        # --Insert Movie--
        batch_size = 51 - Movie.objects.count()
        if batch_size > 0:
            objs = (Movie(name='Movie_{0}'.format(i)) for i in range(1, batch_size))
            Movie.objects.bulk_create(objs, batch_size)

        # --Insert ViewsMovie--
        users_id_items = User.objects.values_list('id', flat=True)
        len_users = len(users_id_items)
        movies_id_items = Movie.objects.values_list('id', flat=True)
        len_movies = len(movies_id_items)
        batch_size = 500000 - ViewsMovie.objects.count()

        objs = (ViewsMovie(user_id=users_id_items[random.randrange(len_users)],
                           movie_id=movies_id_items[random.randrange(len_movies)]
                           ) for _ in range(batch_size)
                )
        ViewsMovie.objects.bulk_create(objs, batch_size, ignore_conflicts=True)

        self.stdout.write(self.style.SUCCESS('Successfully load data '))
