from django.urls import path

from . import views

urlpatterns = [
    path(r'', views.Homepage.as_view(), name='homepage')
]
