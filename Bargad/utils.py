import os
import uuid
from functools import partial
from functools import wraps

from django.http import Http404, HttpResponseRedirect
from django.urls import reverse


def get_image_file_path(folder_name, instance, filename):
    # Do not want store files by the same name user did. Just preventing some future embarrassment.
    _, filename_ext = os.path.splitext(filename)
    filename = f"{uuid.uuid4()}{filename_ext}"

    return os.path.join(folder_name, filename)


# Keeping profile_images, post media and comment media in separate folders.
get_profile_image_file_path = partial(get_image_file_path, 'profile_pictures')

get_post_image_file_path = partial(get_image_file_path, 'post_images')
get_post_gif_file_path = partial(get_image_file_path, 'post_gifs')
get_post_video_file_path = partial(get_image_file_path, 'post_videos')
get_post_audio_file_path = partial(get_image_file_path, 'post_audios')
get_post_document_file_path = partial(get_image_file_path, 'post_documents')
get_post_attachment_file_path = partial(get_image_file_path, 'post_attachments')

get_comment_image_file_path = partial(get_image_file_path, 'comment_images')
get_comment_gif_file_path = partial(get_image_file_path, 'comment_gifs')
get_comment_video_file_path = partial(get_image_file_path, 'comment_videos')
get_comment_audio_file_path = partial(get_image_file_path, 'comment_audios')
get_comment_document_file_path = partial(get_image_file_path, 'comment_documents')
get_comment_attachment_file_path = partial(get_image_file_path, 'comment_attachments')


# Decorators for allowing access to views based on user type.
def bargad_user_login_required(user_type=None):
    def decorator(a_view):
        @wraps(a_view)
        def _wrapped_view(request, *args, **kwargs):
            if not request.student.is_authenticated:
                return HttpResponseRedirect(reverse('login-page'))

            if user_type is None:
                return a_view(request, *args, **kwargs)

            if (user_type == 'Admin' and request.student.is_user_admin) or \
                    (user_type == 'Staff' and request.student.is_user_staff) or \
                    (user_type == 'Student' and request.student.is_user_student):
                return a_view(request, *args, **kwargs)

            raise Http404('page not found!')

        return _wrapped_view

    return decorator
