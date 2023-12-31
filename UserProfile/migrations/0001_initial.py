# Generated by Django 5.0 on 2023-12-11 23:11

import Bargad.utils
import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
import functools
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Academic', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfileBase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dob', models.DateField(blank=True, verbose_name='Date of Birth')),
                ('gender', models.PositiveSmallIntegerField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], verbose_name='gender')),
                ('bio', models.CharField(blank=True, max_length=256, verbose_name='bio')),
                ('correspondence_address', models.TextField(blank=True, max_length=1024, verbose_name='correspondence address')),
                ('permanent_address', models.TextField(blank=True, max_length=1024, verbose_name='permanent address')),
                ('primary_contact', models.CharField(blank=True, max_length=15, verbose_name='primary contact')),
                ('secondary_contact', models.CharField(blank=True, max_length=15, verbose_name='secondary contact')),
                ('father_name', models.CharField(blank=True, max_length=120, verbose_name='father name')),
                ('father_qualification', models.CharField(blank=True, max_length=120, verbose_name='father qualification')),
                ('father_contact', models.CharField(blank=True, max_length=15, verbose_name='father contact')),
                ('mother_name', models.CharField(blank=True, max_length=120, verbose_name='mother name')),
                ('mother_qualification', models.CharField(blank=True, max_length=120, verbose_name='mother qualification')),
                ('mother_contact', models.CharField(blank=True, max_length=15, verbose_name='mother contact')),
                ('guardian_name', models.CharField(blank=True, max_length=120, verbose_name='guardian name')),
                ('guardian_contact', models.CharField(blank=True, max_length=15, verbose_name='guardian contact')),
            ],
        ),
        migrations.CreateModel(
            name='BargadUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_type', models.CharField(choices=[('Admin', 'Admin'), ('Dean', 'Dean'), ('Head of Department', 'Hod'), ('Staff', 'Staff'), ('Teacher', 'Teacher'), ('Student', 'Student'), ('Alumni', 'Alumni')], default='Student', max_length=32, verbose_name='user type')),
                ('profile_picture', models.ImageField(blank=True, upload_to=functools.partial(Bargad.utils.get_image_file_path, *('profile_pictures',), **{}), verbose_name='profile picture')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='StaffUserProfile',
            fields=[
                ('userprofilebase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='UserProfile.userprofilebase')),
                ('post', models.CharField(blank=True, max_length=120, verbose_name='post')),
                ('staff', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='staff_profile', to=settings.AUTH_USER_MODEL)),
            ],
            bases=('UserProfile.userprofilebase',),
        ),
        migrations.CreateModel(
            name='StudentUserProfile',
            fields=[
                ('userprofilebase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='UserProfile.userprofilebase')),
                ('is_alumni', models.BooleanField(default=False, verbose_name='is alumni')),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='Academic.program')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='Academic.section')),
                ('semester', models.ManyToManyField(related_name='students', to='Academic.semester')),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student_profile', to=settings.AUTH_USER_MODEL)),
                ('subject', models.ManyToManyField(related_name='students', to='Academic.subject')),
            ],
            bases=('UserProfile.userprofilebase',),
        ),
        migrations.CreateModel(
            name='TeacherUserProfile',
            fields=[
                ('userprofilebase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='UserProfile.userprofilebase')),
                ('qualification', models.CharField(blank=True, max_length=120, verbose_name='qualification')),
                ('experience', models.CharField(blank=True, max_length=120, verbose_name='experience')),
                ('designation', models.CharField(blank=True, max_length=120, verbose_name='designation')),
                ('subject', models.ManyToManyField(related_name='teachers', to='Academic.subject')),
                ('teacher', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='teacher_profile', to=settings.AUTH_USER_MODEL)),
            ],
            bases=('UserProfile.userprofilebase',),
        ),
    ]
