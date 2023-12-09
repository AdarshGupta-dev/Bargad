from django.contrib import admin

from UserProfile.models import UserProfileBase, BargadUser, StudentUserProfile, StaffUserProfile, TeacherUserProfile

admin.site.register(UserProfileBase)
admin.site.register(BargadUser)
admin.site.register(StudentUserProfile)
admin.site.register(StaffUserProfile)
admin.site.register(TeacherUserProfile)
