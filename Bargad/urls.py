from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

import SocialMedia.views

urlpatterns = [
    path(r'', include(('SocialMedia.urls', 'SocialMedia'), namespace='social-media')),
    path(r'dashboard/', include(('Dashboard.urls', 'Dashboard'), namespace='dashboard')),
    path(r'post/', include(('Post.urls', 'Post'), namespace='post')),
    # path(r'^chat/', include(('Chat.urls', 'Chat'), namespace='social-media')),

    # global urls
    path(r'login/', SocialMedia.views.Login.as_view(), name='login-page'),
    path(r'logout/', SocialMedia.views.Logout.as_view(), name='logout'),

    # admin page
    path(r'internal/admin/', admin.site.urls),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
