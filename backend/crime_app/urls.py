from django.urls import path
from crime_app.views import (query1, query5)

urlpatterns = [
    path('query1/', query1.as_view(), name='query1'),
    path('query5/', query5.as_view(), name='query5')
]