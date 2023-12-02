from django.urls import path

from . import views

urlpatterns = [
    path(r'api/create_post/', views.PostCreateView.as_view(), name='create-post-api'),
]
