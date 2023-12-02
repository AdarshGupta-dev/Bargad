from django.contrib import admin

from UserProfile.models import UserProfile, BargadUser, StudentUserProfile, StaffUserProfile, TeacherUserProfile

admin.site.register(UserProfile)
admin.site.register(BargadUser)
admin.site.register(StudentUserProfile)
admin.site.register(StaffUserProfile)
admin.site.register(TeacherUserProfile)
