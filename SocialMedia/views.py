from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from Bargad.email_backend import EmailBackend
from Bargad.utils import bargad_user_login_required
from Post.models import Post


class Login(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'login-page.html')

    def post(self, *args, **kwargs):
        request = self.request
        username = self.request.POST.get('email')
        password = self.request.POST.get('password')

        user = EmailBackend().authenticate(username, password)

        if not user:
            messages.error(request, "Either Email or Password is invalid")
            return redirect(reverse('login-page'))

        login(self.request, user)
        return redirect(reverse('social-media:homepage'))


class Logout(View):
    def get(self, *args, **kwargs):
        logout(self.request)
        return render(self.request, 'login-page.html')


class Homepage(View):

    @method_decorator(bargad_user_login_required())
    def get(self, *args, **kwargs):
        posts = list(Post.objects.all())
        context_dict = {
            'posts': posts
        }
        return render(self.request, 'SocialMedia/social-media-base.html', context_dict)
