import factory

from django.contrib.auth.models import User


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    @factory.sequence
    def email(n):
        return 'user_%d@test.ru' % n

    @factory.sequence
    def username(n):
        return 'user_%d' % n
