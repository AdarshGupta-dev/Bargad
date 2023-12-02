from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


class EmailBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        user_model = get_user_model()

        qs = Q(email=username) | Q(username=username)
        user = user_model.objects.filter(qs).first()

        if user and user.check_password(password):
            return user
