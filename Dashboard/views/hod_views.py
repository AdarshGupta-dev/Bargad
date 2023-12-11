from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from Academic.models import Program, AcademicSession, Department
from Bargad.utils import bargad_user_login_required
from UserProfile.models import StudentUserProfile, StaffUserProfile, TeacherUserProfile


class HodHomepage(View):
    @method_decorator(bargad_user_login_required(user_type='Admin'))
    def get(self, *args, **kwargs):
        return render(self.request, 'Dashboard/hod/hod-dashboard-home.html')


class AcademicSessions(View):
    @method_decorator(bargad_user_login_required(user_type='Admin'))
    def get(self, *args, **kwargs):
        academic_sessions = AcademicSession.objects.all()
        context_dict = {
            'academic_sessions': academic_sessions,
        }
        return render(self.request, 'Dashboard/hod/academic-sessions.html', context_dict)


class AddAcademicSession(View):
    @method_decorator(bargad_user_login_required(user_type='Admin'))
    def get(self, *args, **kwargs):
        return render(self.request, 'Dashboard/hod/add-academic-session.html')

    @method_decorator(bargad_user_login_required(user_type='Admin'))
    def post(self, *args, **kwargs):
        start_date = self.request.POST.get('start-date')
        end_date = self.request.POST.get('end-date')
        AcademicSession.objects.create(start_date=start_date, end_date=end_date)
        return redirect(reverse('dashboard:list-academic-session'))


class EditAcademicSession(View):
    @method_decorator(bargad_user_login_required(user_type='Admin'))
    def get(self, *args, **kwargs):
        academic_session_id = kwargs.get('academic_session_id')
        academic_session = AcademicSession.objects.get(pk=academic_session_id)
        academic_session.start_date = academic_session.start_date.strftime('%Y-%m-%d')
        academic_session.end_date = academic_session.end_date.strftime('%Y-%m-%d')

        context_dict = {
            'academic_session': academic_session,
        }

        return render(self.request, 'Dashboard/hod/edit-academic-session-data.html', context_dict)

    @method_decorator(bargad_user_login_required(user_type='Admin'))
    def post(self, *args, **kwargs):
        academic_session_id = kwargs.get('academic_session_id')
        start_date = self.request.POST.get('start-date')
        end_date = self.request.POST.get('end-date')

        academic_session = AcademicSession.objects.get(pk=academic_session_id)
        academic_session.start_date = start_date
        academic_session.end_date = end_date

        academic_session.save()
        return redirect(reverse('dashboard:list-academic-session'))


class DeleteAcademicSession(View):
    @method_decorator(bargad_user_login_required(user_type='Admin'))
    def get(self, *args, **kwargs):
        academic_session_id = kwargs.get('academic_session_id')
        academic_session = get_object_or_404(AcademicSession.objects, pk=academic_session_id)
        academic_session.delete()
        return redirect(reverse('dashboard:list-academic-session'))


class AddStudent(View):
    @method_decorator(bargad_user_login_required(user_type='Admin'))
    def get(self, *args, **kwargs):
        return render(self.request, 'Dashboard/hod/add-student.html')


class EditStudentData(View):
    @method_decorator(bargad_user_login_required(user_type='Admin'))
    def get(self, *args, **kwargs):
        student_id = kwargs.get('student_id')
        student = StudentUserProfile.objects.get(student_id=student_id)

        context_dict = {
            'student': student,
        }

        return render(self.request, 'Dashboard/hod/edit-student-data.html', context_dict)


class ListStudents(View):
    @method_decorator(bargad_user_login_required(user_type='Admin'))
    def get(self, *args, **kwargs):
        students = StudentUserProfile.objects.all()
        context_dict = {
            'students': students,
        }
        return render(self.request, 'Dashboard/hod/list-student.html', context_dict)


class DeleteStudent(View):
    @method_decorator(bargad_user_login_required(user_type='Admin'))
    def get(self, *args, **kwargs):
        student_id = kwargs.get('student_id')
        student = get_object_or_404(StudentUserProfile.objects, student_id=student_id)
        student.delete()
        return redirect(reverse('dashboard:list-student'))


class AddTeacher(View):
    @method_decorator(bargad_user_login_required(user_type='Admin'))
    def get(self, *args, **kwargs):
        return render(self.request, 'Dashboard/hod/add-teacher.html')


class EditTeacherData(View):
    @method_decorator(bargad_user_login_required(user_type='Admin'))
    def get(self, *args, **kwargs):
        teacher_id = kwargs.get('teacher_id')
        teacher = TeacherUserProfile.objects.get(teacher_id=teacher_id)

        context_dict = {
            'teacher': teacher,
        }

        return render(self.request, 'Dashboard/hod/edit-teacher-data.html', context_dict)


class ListTeachers(View):
    @method_decorator(bargad_user_login_required(user_type='Admin'))
    def get(self, *args, **kwargs):
        teachers = TeacherUserProfile.objects.all()
        context_dict = {
            'teachers': teachers,
        }
        return render(self.request, 'Dashboard/hod/list-teacher.html', context_dict)


class DeleteTeacher(View):
    @method_decorator(bargad_user_login_required(user_type='Admin'))
    def get(self, *args, **kwargs):
        teacher_id = kwargs.get('teacher_id')
        teacher = get_object_or_404(TeacherUserProfile.objects, teacher_id=teacher_id)
        teacher.delete()
        return redirect(reverse('dashboard:list-teacher'))


class AddStaff(View):
    @method_decorator(bargad_user_login_required(user_type='Admin'))
    def get(self, *args, **kwargs):
        return render(self.request, 'Dashboard/hod/add-staff.html')


class EditStaffData(View):
    @method_decorator(bargad_user_login_required(user_type='Admin'))
    def get(self, *args, **kwargs):
        staff_id = kwargs.get('staff_id')
        staff = StaffUserProfile.objects.get(staff_id=staff_id)

        context_dict = {
            'staff': staff,
        }

        return render(self.request, 'Dashboard/hod/edit-staff-data.html', context_dict)


class ListStaff(View):
    @method_decorator(bargad_user_login_required(user_type='Admin'))
    def get(self, *args, **kwargs):
        staffs = StaffUserProfile.objects.all()
        context_dict = {
            'staffs': staffs,
        }
        return render(self.request, 'Dashboard/hod/list-staff.html', context_dict)


class DeleteStaff(View):
    @method_decorator(bargad_user_login_required(user_type='Admin'))
    def get(self, *args, **kwargs):
        staff_id = kwargs.get('staff_id')
        staff = get_object_or_404(StaffUserProfile.objects, staff_id=staff_id)
        staff.delete()
        return redirect(reverse('dashboard:list-staff'))


class ListProgram(View):
    @method_decorator(bargad_user_login_required(user_type='Admin'))
    def get(self, *args, **kwargs):
        Programs = Program.objects.all()
        context_dict = {
            'Programs': Programs,
        }
        return render(self.request, 'Dashboard/hod/list-Program.html', context_dict)


class AddProgram(View):
    @method_decorator(bargad_user_login_required(user_type='Admin'))
    def get(self, *args, **kwargs):
        sessions = Session.objects.all()
        departments = Department.objects.all()

        context_dict = {
            'sessions': sessions,
            'departments': departments,
        }
        return render(self.request, 'Dashboard/hod/add-Program.html', context_dict)

    @method_decorator(bargad_user_login_required(user_type='Admin'))
    def post(self, *args, **kwargs):
        name = self.request.POST.get('Program-shortname')
        Program_code = self.request.POST.get('Program-code')
        session_id = self.request.POST.get('session')
        department_id = self.request.POST.get('department')
        session = Session.objects.get(pk=session_id)
        department = Department.objects.get(department_code=department_id)
        Program.objects.create(name=name, Program_code=Program_code, session=session, department=department)
        return redirect(reverse('dashboard:list-Program'))


class EditProgramData(View):
    @method_decorator(bargad_user_login_required(user_type='Admin'))
    def get(self, *args, **kwargs):
        Program_id = kwargs.get('Program_id')
        Program = Program.objects.get(Program_id=Program_id)

        context_dict = {
            'Program': Program,
        }

        return render(self.request, 'Dashboard/hod/edit-Program-data.html', context_dict)


class DeleteProgram(View):
    @method_decorator(bargad_user_login_required(user_type='Admin'))
    def get(self, *args, **kwargs):
        Program_id = kwargs.get('Program_id')
        Program = get_object_or_404(Program.objects, Program_id=Program_id)
        Program.delete()
        return redirect(reverse('dashboard:list-Program'))


class ListSession(View):
    @method_decorator(bargad_user_login_required(user_type='Admin'))
    def get(self, *args, **kwargs):
        sessions = Session.objects.all()
        context_dict = {
            'sessions': sessions,
        }
        return render(self.request, 'Dashboard/hod/academic-sessions.html', context_dict)


class AddSession(View):
    @method_decorator(bargad_user_login_required(user_type='Admin'))
    def get(self, *args, **kwargs):
        return render(self.request, 'Dashboard/hod/add-session.html')

    @method_decorator(bargad_user_login_required(user_type='Admin'))
    def post(self, *args, **kwargs):
        start_date = self.request.POST.get('start-date')
        end_date = self.request.POST.get('end-date')
        Session.objects.create(start_date=start_date, end_date=end_date)
        return redirect(reverse('dashboard:list-session'))


class EditSessionData(View):
    @method_decorator(bargad_user_login_required(user_type='Admin'))
    def get(self, *args, **kwargs):
        session_id = kwargs.get('session_id')
        session = Session.objects.get(pk=session_id)
        session.start_date = session.start_date.strftime('%Y-%m-%d')
        session.end_date = session.end_date.strftime('%Y-%m-%d')

        context_dict = {
            'session': session,
        }

        return render(self.request, 'Dashboard/hod/edit-session-data.html', context_dict)

    @method_decorator(bargad_user_login_required(user_type='Admin'))
    def post(self, *args, **kwargs):
        session_id = kwargs.get('session_id')
        start_date = self.request.POST.get('start-date')
        end_date = self.request.POST.get('end-date')

        session = Session.objects.get(pk=session_id)
        session.start_date = start_date
        session.end_date = end_date

        session.save()
        return redirect(reverse('dashboard:list-session'))


class DeleteSession(View):
    @method_decorator(bargad_user_login_required(user_type='Admin'))
    def get(self, *args, **kwargs):
        session_id = kwargs.get('session_id')
        session = get_object_or_404(Session.objects, pk=session_id)
        session.delete()
        return redirect(reverse('dashboard:list-session'))


class ListDepartment(View):
    @method_decorator(bargad_user_login_required(user_type='Admin'))
    def get(self, *args, **kwargs):
        departments = Department.objects.all()
        context_dict = {
            'departments': departments,
        }
        return render(self.request, 'Dashboard/hod/list-department.html', context_dict)


class AddDepartment(View):
    @method_decorator(bargad_user_login_required(user_type='Admin'))
    def get(self, *args, **kwargs):
        return render(self.request, 'Dashboard/hod/add-department.html')

    @method_decorator(bargad_user_login_required(user_type='Admin'))
    def post(self, *args, **kwargs):
        name = self.request.POST.get('department-shortname')
        department_code = self.request.POST.get('department-code')
        Department.objects.create(name=name, department_code=department_code)
        return redirect(reverse('dashboard:list-department'))


class EditDepartmentData(View):
    @method_decorator(bargad_user_login_required(user_type='Admin'))
    def get(self, *args, **kwargs):
        department_code = kwargs.get('department_code')
        department = Department.objects.get(department_code=department_code)

        context_dict = {
            'department': department,
        }

        return render(self.request, 'Dashboard/hod/edit-department-data.html', context_dict)

    @method_decorator(bargad_user_login_required(user_type='Admin'))
    def post(self, *args, **kwargs):
        department_name = self.request.POST.get('department-shortname')
        department_code = self.request.POST.get('department-code')

        department = Department.objects.get(department_code=department_code)
        department.short_name = department_name
        department.department_code = department_code

        department.save()
        return redirect(reverse('dashboard:list-department'))


class DeleteDepartment(View):
    @method_decorator(bargad_user_login_required(user_type='Admin'))
    def get(self, *args, **kwargs):
        department_id = kwargs.get('department_id')
        department = get_object_or_404(Department.objects, pk=department_id)
        department.delete()
        return redirect(reverse('dashboard:list-department'))
