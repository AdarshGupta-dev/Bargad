from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from UserProfile.models import StudentUserProfile, TeacherUserProfile


# Academic Session is year from to year to. Like 2018 -> 2022.
class AcademicSession(models.Model):
    start_year = models.PositiveSmallIntegerField(_('start year'), null=False)
    end_year = models.PositiveSmallIntegerField(_('end year'), null=False)

    start_date = models.DateField(_('start date'), null=False)
    end_date = models.DateField(_('end date'), null=False)

    def __str__(self):
        return str(self.start_date.year) + '-' + str(self.end_date.year)

    def is_active(self):
        return self.start_date <= timezone.now().date() <= self.end_date

    def save(self, *args, **kwargs):
        # We will mostly take years as input and calculate dates from them.
        # We still need date as Academic session start month are not same for all universities.

        if not self.start_year:
            raise ValidationError("Academic start year is required")

        if not self.end_year:
            self.end_year = self.start_year + 3

        if self.end_year < self.start_year:
            raise ValidationError("Academic end year can't be less than start year")

        self.start_date = timezone.datetime(self.start_year, 7, 1)
        self.end_date = timezone.datetime(self.end_year, 6, 30)

        super().save(*args, **kwargs)


# Department is grouped by similar subjects.
# e.g. Department of Engineering, Department of Science, Department of Commerce.
class Department(models.Model):
    name = models.CharField(_('name'), max_length=120, blank=False, null=False, unique=True)

    head_of_department = models.ForeignKey(TeacherUserProfile, related_name='departments', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


# Program is a course like B.Tech, M.Tech, B.Sc., M.Sc, B.Com, M.Com.
class Program(models.Model):
    program_id = models.CharField(_('program id'), max_length=10, blank=False, name=False)
    short_name = models.CharField(_('short name'), max_length=120, blank=False, null=False)
    full_name = models.CharField(_('full name'), max_length=120, blank=False, null=False)

    academic_session = models.ForeignKey(AcademicSession, related_name='programs', on_delete=models.CASCADE)
    department = models.ForeignKey(Department, related_name='programs', on_delete=models.CASCADE)

    student_capacity = models.PositiveSmallIntegerField(_('student capacity'), null=False, default=0)

    def __str__(self):
        return self.short_name

    class Meta:
        unique_together = ('program_id', 'academic_session', 'department')


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

    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    semester = models.PositiveSmallIntegerField(_('semester'), choices=SemesterChoices.choices, null=False)

    start_date = models.DateField(_('start date'), null=False)
    end_date = models.DateField(_('end date'), null=False)

    @cached_property
    def is_active(self):
        return self.start_date <= timezone.now().date() <= self.end_date

    def __str__(self):
        return self.program.short_name + ' ' + str(self.semester)

    class Meta:
        unique_together = ('semester', 'program')


class Subject(models.Model):
    subject_code = models.CharField(_('subject code'), max_length=20)

    short_name = models.CharField(_('short name'), max_length=120, blank=False, null=False)
    full_name = models.CharField(_('full name'), max_length=120, blank=False, null=False)

    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)

    def __str__(self):
        return self.subject_code

    class Meta:
        unique_together = ('subject_code', 'program')


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

    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    section = models.CharField(_('section'), max_length=1, choices=SectionChoices.choices, null=False, default=SectionChoices.A)

    def __str__(self):
        return f"{self.program.short_name} {self.semester.semester} {self.section}"

    class Meta:
        unique_together = ('program', 'semester', 'section')


class Period(models.Model):
    """
    Session is period/class held on a particular date.
    """

    class PeriodChoices(models.IntegerChoices):
        SESSION_1 = 1
        SESSION_2 = 2
        SESSION_3 = 3
        SESSION_4 = 4
        SESSION_5 = 5
        SESSION_6 = 6
        SESSION_7 = 7
        SESSION_8 = 8
        SESSION_9 = 9
        SESSION_10 = 10

    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

    date = models.DateField(_('date'), null=False, db_index=True)
    period = models.PositiveSmallIntegerField(_('session'), choices=PeriodChoices.choices, null=False)

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(TeacherUserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date} - {self.period}"

    class Meta:
        unique_together = ('program', 'semester', 'section', 'date', 'period')


class TeacherAttendance(models.Model):
    """
    Attendance is a record of a student/teacher/staff presence on a particular day.
    Leave applied by student/teacher/staff will be recorded here.
    """

    class AttendanceChoices(models.IntegerChoices):
        PRESENT = 1
        ABSENT = 2
        LATE = 3
        LEAVE = 4

    date = models.DateField(_('date'), null=False, db_index=True)
    teacher = models.ForeignKey(TeacherUserProfile, related_name="attendance", on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(_('status'), choices=AttendanceChoices.choices, null=False)

    def __str__(self):
        return f"{self.teacher.full_name} - {self.date} {self.status}"

    class Meta:
        unique_together = ('date', 'teacher')


class StudentAttendance(models.Model):
    """
    StudentAttendance is a record of a student presence on a particular day throughout the periods.
    """

    class AttendanceChoices(models.IntegerChoices):
        PRESENT = 1
        ABSENT = 2

    session = models.ForeignKey(Period, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentUserProfile, related_name="attendance", on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(_('status'), choices=AttendanceChoices.choices, null=False)

    def __str__(self):
        return f"{self.student.full_name} - {self.session} {self.status}"

    class Meta:
        unique_together = ('session', 'student')


class Grade(models.Model):
    student = models.ForeignKey(StudentUserProfile, related_name="grade", on_delete=models.CASCADE, db_index=True)
    teacher = models.ForeignKey(TeacherUserProfile, related_name="graded", on_delete=models.CASCADE)

    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    marks = models.PositiveSmallIntegerField(_('marks'), null=False, validators=[MaxValueValidator(100), MinValueValidator(0)])
    remarks = models.CharField(_('remarks'), max_length=256, blank=True, null=False)

    def __str__(self):
        return f"{self.student.full_name} - {self.semester} {self.subject} {self.marks}"

    class Meta:
        unique_together = ('student', 'semester', 'subject')
