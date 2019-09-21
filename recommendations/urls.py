from django.urls import re_path
from .views import CollaborativeView, SimpleSqlView

urlpatterns = [
    re_path(r'^simple_sql/$', SimpleSqlView.as_view(), name='simple_sql'),
    re_path(r'^collaborative/$', CollaborativeView.as_view(), name='collaborative'),
]
