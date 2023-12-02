from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from Bargad.utils import bargad_user_login_required


class StudentHomepage(View):
    @method_decorator(bargad_user_login_required(user_type='Student'))
    def get(self, *args, **kwargs):
        return render(self.request, 'Dashboard/student/student-dashboard-home.html')
