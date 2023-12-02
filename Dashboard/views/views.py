from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from Bargad.utils import bargad_user_login_required


class Homepage(View):
    @method_decorator(bargad_user_login_required())
    def get(self, *args, **kwargs):
        if self.request.user.is_user_admin:
            return redirect(reverse('dashboard:hod-homepage'))

        if self.request.user.is_user_staff:
            return redirect(reverse('dashboard:staff-homepage'))

        if self.request.user.is_user_student:
            return redirect(reverse('dashboard:student-homepage'))

        raise Http404('page not found!')


class UpdateProfile(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'Dashboard/profile-page.html')

    def post(self, *args, **kwargs):
        first_name = self.request.POST.get('first_name')
        last_name = self.request.POST.get('last_name')
        profile_picture = self.request.FILES.get('profile_picture')

        password = self.request.POST.get('password')

        try:
            user = CustomUser.objects.get(pk=self.request.user.id)

            user.first_name = first_name
            user.last_name = last_name

            if profile_picture:
                user.profile_picture = profile_picture

            if password:
                user.set_password(password)

            user.save()

        except:
            messages.success(self.request, "Something went wrong. Please try again after some time.")
        finally:
            messages.success(self.request, "Your Profile has been updated successfully.")

        return redirect('profile-page')
