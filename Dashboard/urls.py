from django.urls import path

from .views import staff_views, student_views, hod_views, views
urlpatterns = [
    # common views
    path(r'', views.Homepage.as_view(), name='homepage'),
    path(r'profile/', views.UpdateProfile.as_view(), name='profile-page'),

    # Hod views
    path(r'hod/', hod_views.HodHomepage.as_view(), name='hod-homepage'),

    # academic session CRUD
    path(r'academic-sessions/', hod_views.AcademicSessions.as_view(), name='academic-sessions'),
    path(r'academic-sessions/add/', hod_views.AddAcademicSession.as_view(), name='add-academic-session'),
    path(r'academic-sessions/edit/<academic_session_id>', hod_views.EditAcademicSession.as_view(), name='edit-academic-session'),
    path(r'academic-sessions/delete/<academic_session_id>', hod_views.DeleteAcademicSession.as_view(), name='delete-academic-session'),


    path(r'hod/list-session/', hod_views.ListSession.as_view(), name='list-session'),
    path(r'hod/add-session/', hod_views.AddSession.as_view(), name='add-session'),
    path(r'hod/edit-session-data/<session_id>', hod_views.EditSessionData.as_view(), name='edit-session-data'),
    path(r'hod/delete-session/<session_id>', hod_views.DeleteSession.as_view(), name='delete-session'),

    path(r'hod/list-student/', hod_views.ListStudents.as_view(), name='list-student'),
    path(r'hod/add-student/', hod_views.AddStudent.as_view(), name='add-student'),
    path(r'hod/edit-student-data/<student_id>', hod_views.EditStudentData.as_view(), name='edit-student-data'),
    path(r'hod/delete-student/<student_id>', hod_views.DeleteStudent.as_view(), name='delete-student'),

    path(r'hod/list-teacher/', hod_views.ListTeachers.as_view(), name='list-teacher'),
    path(r'hod/add-teacher/', hod_views.AddTeacher.as_view(), name='add-teacher'),
    path(r'hod/edit-teacher-data/<teacher_id>', hod_views.EditTeacherData.as_view(), name='edit-teacher-data'),
    path(r'hod/delete-teacher/<teacher_id>', hod_views.DeleteTeacher.as_view(), name='delete-teacher'),

    path(r'hod/list-staff/', hod_views.ListStaff.as_view(), name='list-staff'),
    path(r'hod/add-staff/', hod_views.AddStaff.as_view(), name='add-staff'),
    path(r'hod/edit-staff-data/<staff_id>', hod_views.EditStaffData.as_view(), name='edit-staff-data'),
    path(r'hod/delete-staff/<staff_id>', hod_views.DeleteStaff.as_view(), name='delete-staff'),



    path(r'hod/list-department/', hod_views.ListDepartment.as_view(), name='list-department'),
    path(r'hod/add-department/', hod_views.AddDepartment.as_view(), name='add-department'),
    path(r'hod/edit-department-data/<department_code>', hod_views.EditDepartmentData.as_view(), name='edit-department-data'),
    path(r'hod/delete-department/<department_code>', hod_views.DeleteDepartment.as_view(), name='delete-department'),

    path(r'hod/list-program/', hod_views.ListProgram.as_view(), name='list-program'),
    path(r'hod/add-program/', hod_views.AddProgram.as_view(), name='add-program'),
    path(r'hod/edit-program-data/<program_code>', hod_views.EditProgramData.as_view(), name='edit-program-data'),
    path(r'hod/delete-program/<program_code>', hod_views.DeleteProgram.as_view(), name='delete-program'),

    # Staff views
    path(r'staff/', staff_views.StaffHomepage.as_view(), name='staff-homepage'),

    # Student views
    path(r'student/', student_views.StudentHomepage.as_view(), name='student-homepage'),
]

