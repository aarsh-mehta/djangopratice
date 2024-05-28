from django.urls import path
from .views import PersonAPI

urlpatterns = [
    path('persons', PersonAPI.as_view(), name='person_list_create'),
    path('persons/<int:person_id>', PersonAPI.as_view(), name='person_detail'),
]
