from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from Bargad.utils import bargad_user_login_required


class StaffHomepage(View):
    @method_decorator(bargad_user_login_required(user_type='Staff'))
    def get(self, *args, **kwargs):
        return render(self.request, 'Dashboard/staff/staff-dashboard-home.html')
