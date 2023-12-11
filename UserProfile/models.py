from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from Bargad.utils import get_profile_image_file_path


class BargadUser(AbstractUser):
    """
    Custom User Model. We will use this instead of django's default User model.
    """
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
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

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

    @cached_property
    def get_profile_picture_url(self):
        if self.profile_picture:
            return self.profile_picture.url

        return self.default_profile_picture

    def __str__(self):
        return f"{self.full_name}({self.username}) - {self.user_type}"


class UserProfileBase(models.Model):
    """
    I wish to keep our auth model, BargadUser, to base minimum.
    Everything that is not mandatory will be here in BaseUserProfile.
    StudentUserProfile, TeacherUserProfile, StaffUserProfile will inherit from this and extend themselves as needed.
    Note: This is not an abstract model. Don't use it directly.
    """

    class GenderChoices(models.TextChoices):
        MALE = 'Male'
        FEMALE = 'Female'
        OTHER = 'Other'

    dob = models.DateField(_('Date of Birth'), blank=True, null=False)
    gender = models.PositiveSmallIntegerField(_('gender'), blank=True, null=False, choices=GenderChoices.choices)

    bio = models.CharField(_('bio'), max_length=256, blank=True, null=False)

    correspondence_address = models.TextField(_('correspondence address'), max_length=1024, blank=True, null=False)
    permanent_address = models.TextField(_('permanent address'), max_length=1024, blank=True, null=False)

    primary_contact = models.CharField(_('primary contact'), max_length=15, blank=True, null=False)
    secondary_contact = models.CharField(_('secondary contact'), max_length=15, blank=True, null=False)

    # parent/guardian details
    father_name = models.CharField(_('father name'), max_length=120, blank=True, null=False)
    father_qualification = models.CharField(_('father qualification'), max_length=120, blank=True, null=False)
    father_contact = models.CharField(_('father contact'), max_length=15, blank=True, null=False)

    mother_name = models.CharField(_('mother name'), max_length=120, blank=True, null=False)
    mother_qualification = models.CharField(_('mother qualification'), max_length=120, blank=True, null=False)
    mother_contact = models.CharField(_('mother contact'), max_length=15, blank=True, null=False)

    guardian_name = models.CharField(_('guardian name'), max_length=120, blank=True, null=False)
    guardian_contact = models.CharField(_('guardian contact'), max_length=15, blank=True, null=False)


class StudentUserProfile(UserProfileBase):
    student = models.OneToOneField(get_user_model(), related_name='student_profile', on_delete=models.CASCADE, db_index=True)

    is_alumni = models.BooleanField(_('is alumni'), null=False, default=False)

    program = models.ForeignKey('Academic.Program', related_name='students', on_delete=models.CASCADE)
    semester = models.ManyToManyField('Academic.Semester', related_name='students')
    subject = models.ManyToManyField('Academic.Subject', related_name='students')
    section = models.ForeignKey('Academic.Section', related_name='students', on_delete=models.CASCADE)

    def __str__(self):
        return 'ST-' + str(self.student_id)

    @cached_property
    def full_name(self):
        return f"{self.student.first_name} {self.student.last_name}"


class TeacherUserProfile(UserProfileBase):
    teacher = models.OneToOneField(get_user_model(), related_name='teacher_profile', on_delete=models.CASCADE, db_index=True)

    qualification = models.CharField(_('qualification'), max_length=120, blank=True, null=False)
    experience = models.CharField(_('experience'), max_length=120, blank=True, null=False)
    designation = models.CharField(_('designation'), max_length=120, blank=True, null=False)

    subject = models.ManyToManyField('Academic.Subject', related_name='teachers')

    def __str__(self):
        return 'TE-' + str(self.teacher_id)

    @cached_property
    def full_name(self):
        return f"{self.teacher.first_name} {self.teacher.last_name}"


class StaffUserProfile(UserProfileBase):
    staff = models.OneToOneField(get_user_model(), related_name='staff_profile', on_delete=models.CASCADE, db_index=True)

    post = models.CharField(_('post'), max_length=120, blank=True, null=False)

    def __str__(self):
        return 'SF-' + str(self.staff_id)

    @cached_property
    def full_name(self):
        return f"{self.staff.first_name} {self.staff.last_name}"
