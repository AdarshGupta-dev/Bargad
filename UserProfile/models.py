from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from Bargad.utils import get_profile_image_file_path


# Session is year from to year to. Like 2018 -> 2022.
class Session(models.Model):
    start_date = models.DateField(_('start date'), null=False)
    end_date = models.DateField(_('end date'), null=False)

    def __str__(self):
        return str(self.start_date.year) + '-' + str(self.end_date.year)

    def is_active(self):
        return self.start_date <= timezone.now().date() <= self.end_date

    def clean(self):
        if self.end_date <= self.start_date:
            raise ValidationError("End date must be after start date")

    def save(self, *args, **kwargs):
        self.clean()
        super(Session, self).save(*args, **kwargs)


# Department is grouped by similar subjects.
# department of engineering, department of science, department of commerce.
class Department(models.Model):
    name = models.CharField(_('short name'), max_length=120, blank=False, null=False)

    def __str__(self):
        return self.name


# Program is a course like B.Tech, M.Tech, B.Sc., M.Sc, B.Com, M.Com.
class Program(models.Model):
    short_name = models.CharField(_('short name'), max_length=120, blank=False, null=False)
    full_name = models.CharField(_('full name'), max_length=120, blank=False, null=False)

    session = models.ForeignKey(Session, related_name='programs', on_delete=models.CASCADE)
    department = models.ForeignKey(Department, related_name='programs', on_delete=models.CASCADE)

    def __str__(self):
        return self.short_name


# Semester is a part of a program. Like B.Tech has 8 semesters. M.Tech has 4 semesters.
class Semester(models.Model):
    class SemesterChoices(models.IntegerChoices):
        SEMESTER_1 = 1
        SEMESTER_2 = 2
        SEMESTER_3 = 3
        SEMESTER_4 = 4
        SEMESTER_5 = 5
        SEMESTER_6 = 6
        SEMESTER_7 = 7
        SEMESTER_8 = 8
        SEMESTER_9 = 9
        SEMESTER_10 = 10

    semester = models.PositiveSmallIntegerField(_('semester'), choices=SemesterChoices.choices, null=False)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)

    def __str__(self):
        return self.program.short_name + ' ' + str(self.semester)


class Subject(models.Model):
    code = models.CharField(_('subject code'), primary_key=True, max_length=20)

    short_name = models.CharField(_('short name'), max_length=120, blank=False, null=False)
    full_name = models.CharField(_('full name'), max_length=120, blank=False, null=False)

    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)

    def __str__(self):
        return self.code


class Section(models.Model):
    class SectionChoices(models.TextChoices):
        A = 'A'
        B = 'B'
        C = 'C'
        D = 'D'
        E = 'E'
        F = 'F'
        G = 'G'
        H = 'H'
        I = 'I'
        J = 'J'
        K = 'K'
        L = 'L'
        M = 'M'
        N = 'N'
        O = 'O'
        P = 'P'
        Q = 'Q'
        R = 'R'
        S = 'S'
        T = 'T'
        U = 'U'
        V = 'V'
        W = 'W'
        X = 'X'
        Y = 'Y'
        Z = 'Z'

    section = models.CharField(_('section'), max_length=1, choices=SectionChoices.choices, null=False)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.program.session + ' ' + self.program.short_name + ' ' + self.section


# Custom User Model. We will use this instead of django's default User model.
class BargadUser(AbstractUser):
    default_profile_picture = '/static/assets/img/default_profile_picture.png'

    class UserTypeChoices(models.TextChoices):
        ADMIN = 'Admin',
        DEAN = 'Dean',
        HOD = 'Head of Department',
        STAFF = 'Staff',
        TEACHER = 'Teacher',
        STUDENT = 'Student',
        ALUMNI = 'Alumni',

    UT_ADMIN_LIST = [UserTypeChoices.ADMIN, UserTypeChoices.DEAN, UserTypeChoices.HOD]
    UT_STAFF_LIST = [UserTypeChoices.TEACHER, UserTypeChoices.STAFF]

    user_type = models.CharField(_('user type'), default=UserTypeChoices.STUDENT, choices=UserTypeChoices.choices, max_length=32)
    profile_picture = models.ImageField(_('profile picture'), blank=True, upload_to=get_profile_image_file_path)

    @cached_property
    def is_user_admin(self):
        return self.user_type in self.UT_ADMIN_LIST

    @cached_property
    def is_user_staff(self):
        return self.user_type in self.UT_STAFF_LIST

    @cached_property
    def is_user_student(self):
        return self.user_type == self.UserTypeChoices.STUDENT

    @cached_property
    def is_user_alumni(self):
        return self.user_type == self.UserTypeChoices.ALUMNI

    def get_profile_picture_url(self):
        if self.profile_picture:
            return self.profile_picture.url

        return self.default_profile_picture


class UserProfile(models.Model):
    """
    I wish to keep our auth model, BargadUser, to base minimum.
    Everything that is not mandatory will be here in BaseUserProfile.
    StudentUserProfile, TeacherUserProfile, StaffUserProfile will inherit from this and extend themselves as needed.
    """

    class GenderChoices(models.TextChoices):
        MALE = 'Male'
        FEMALE = 'Female'
        OTHER = 'Other'

    user = models.OneToOneField(get_user_model(), primary_key=True, related_name='profile', on_delete=models.CASCADE, db_index=True)

    dob = models.DateField(_('Date of Birth'), blank=True, null=False)
    gender = models.PositiveSmallIntegerField(_('gender'), blank=True, null=False, choices=GenderChoices.choices)

    c_address = models.TextField(_('correspondence address'), max_length=1024, blank=True, null=False)
    p_address = models.TextField(_('permanent address'), max_length=1024, blank=True, null=False)

    p_contact = models.CharField(_('primary contact'), max_length=15, blank=True, null=False)
    s_contact = models.CharField(_('secondary contact'), max_length=15, blank=True, null=False)

    bio = models.CharField(_('bio'), max_length=256, blank=True, null=False)


class StudentUserProfile(UserProfile):
    student_id = models.AutoField(_('student id'), primary_key=True)

    program = models.ForeignKey(Program, related_name='students', on_delete=models.CASCADE)
    subject = models.ManyToManyField(Subject, related_name='students')

    is_alumni = models.BooleanField(_('is alumni'), null=False, default=False)

    father_name = models.CharField(_('father name'), max_length=120, blank=True, null=False)
    father_qualification = models.CharField(_('father qualification'), max_length=120, blank=True, null=False)
    father_contact = models.CharField(_('father contact'), max_length=15, blank=True, null=False)

    mother_name = models.CharField(_('mother name'), max_length=120, blank=True, null=False)
    mother_qualification = models.CharField(_('mother qualification'), max_length=120, blank=True, null=False)
    mother_contact = models.CharField(_('mother contact'), max_length=15, blank=True, null=False)

    guardian_name = models.CharField(_('guardian name'), max_length=120, blank=True, null=False)
    guardian_contact = models.CharField(_('guardian contact'), max_length=15, blank=True, null=False)

    def __str__(self):
        return 'ST-' + str(self.student_id)


class TeacherUserProfile(UserProfile):
    teacher_id = models.AutoField(_('teacher id'), primary_key=True)

    qualification = models.CharField(_('qualification'), max_length=120, blank=True, null=False)
    experience = models.CharField(_('experience'), max_length=120, blank=True, null=False)
    designation = models.CharField(_('designation'), max_length=120, blank=True, null=False)

    subject = models.ManyToManyField(Subject, related_name='teachers')

    def __str__(self):
        return 'TE-' + str(self.teacher_id)


class StaffUserProfile(UserProfile):
    staff_id = models.AutoField(_('staff id'), primary_key=True)
    post = models.CharField(_('post'), max_length=120, blank=True, null=False)

    def __str__(self):
        return 'SF-' + str(self.staff_id)
