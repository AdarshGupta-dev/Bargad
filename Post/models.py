import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from Bargad.utils import get_post_image_file_path, get_post_gif_file_path, get_post_video_file_path, \
    get_post_audio_file_path, get_post_document_file_path, get_post_attachment_file_path, get_comment_image_file_path, \
    get_comment_gif_file_path, get_comment_video_file_path, get_comment_audio_file_path, get_comment_document_file_path, \
    get_comment_attachment_file_path


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(get_user_model(), related_name='post', on_delete=models.CASCADE)

    caption = models.CharField(_('caption'), max_length=120, null=False, blank=False)
    description = models.CharField(_('description'), max_length=520, null=True, blank=True)

    # each post can be shared. Once post is shared new object will be generated. This will keep track of origin post.
    # shared_from will point to origin of post. shared_to will point to newer version of post.
    shared_from = models.ForeignKey('self', related_name='shared_to', blank=True, null=True, on_delete=models.CASCADE)
    share_count = models.PositiveIntegerField(_('No of times post has been shared'), null=False, default=0)

    # each time post is edited, a new post will be generated. This will keep copy of original post.
    # original_post will point to previous version of post. edited_post will point to newer version of post.
    is_edited = models.BooleanField(_('is edited'), null=False, default=False)
    original_post = models.ForeignKey('self', related_name='edited_post', blank=True, null=True, on_delete=models.CASCADE)
    edit_count = models.PositiveIntegerField(_('No of times post has been edited'), null=False, default=0)

    like_count = models.PositiveIntegerField(_('No of likes'), null=False, default=0)
    comment_count = models.PositiveIntegerField(_('No of comments'), null=False, default=0)

    created_at = models.DateTimeField(_('created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated'), auto_now=True)

    def __str__(self):
        return self.caption


class LikeDislikePost(models.Model):
    class VoteChoices(models.IntegerChoices):
        LIKE = 1, 'Like'
        DISLIKE = -1, 'Dislike'

    post = models.ForeignKey(Post, related_name='vote', on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), related_name='voted_post', on_delete=models.CASCADE)
    value = models.SmallIntegerField(choices=VoteChoices.choices)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(get_user_model(), related_name='comment', on_delete=models.CASCADE)

    text = models.CharField(_('caption'), max_length=120, null=True, blank=True)

    # comment can be an image, gif or video. Quantity of each is 1 at max. i.e. comment will not have 2 images.
    # thus unlike post model, comment model will not have separate model for each type of media.
    image = models.ImageField(_('comment image'), null=True, blank=True, upload_to=get_comment_image_file_path)
    gif = models.FileField(_('comment gif'), null=True, blank=True, upload_to=get_comment_gif_file_path)
    video = models.FileField(_('comment video'), null=True, blank=True, upload_to=get_comment_video_file_path)
    audio = models.FileField(_('comment audio'), null=True, blank=True, upload_to=get_comment_audio_file_path)
    document = models.FileField(_('comment document'), null=True, blank=True, upload_to=get_comment_document_file_path)
    attachment = models.FileField(_('comment attachment'), null=True, blank=True, upload_to=get_comment_attachment_file_path)

    # each time comment is edited, a new comment will be generated. This will keep copy of original comment.
    # original_comment will point to previous version of comment. edited_comment will point to newer version of post.
    is_edited = models.BooleanField(_('is edited'), null=False, default=False)
    original_comment = models.ForeignKey('self', related_name='edited_comment', blank=True, null=True,
                                         on_delete=models.CASCADE)
    edit_count = models.PositiveIntegerField(_('No of times comment has been edited'), null=False, default=0)

    like_count = models.PositiveIntegerField(_('No of likes'), null=False, default=0)
    comment_count = models.PositiveIntegerField(_('No of comments'), null=False, default=0)

    created_at = models.DateTimeField(_('created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated'), auto_now=True)


class LikeDislikeComment(models.Model):
    class VoteChoices(models.IntegerChoices):
        LIKE = 1, 'Like'
        DISLIKE = -1, 'Dislike'

    comment = models.ForeignKey(Comment, related_name='vote', on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), related_name='voted_comment', on_delete=models.CASCADE)
    value = models.SmallIntegerField(choices=VoteChoices.choices)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)


class PostTag(models.Model):
    tag = models.CharField(_('tag'), max_length=120, null=False, blank=False, unique=True, db_index=True)
    post = models.ManyToManyField(Post, related_name='tag')


class PostImages(models.Model):
    """
    This model will store all the images of a post. Each post can have multiple images.
    """
    post = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(_('post image'), null=False, blank=False, upload_to=get_post_image_file_path)


class PostGifs(models.Model):
    """
    This model will store all the gifs of a post. Each post can have multiple gifs.
    """
    post = models.ForeignKey(Post, related_name='gifs', on_delete=models.CASCADE)
    gif = models.FileField(_('post gif'), null=False, blank=False, upload_to=get_post_gif_file_path)


class PostVideos(models.Model):
    """
    This model will store all the videos of a post. Each post can have multiple videos.
    """
    post = models.ForeignKey(Post, related_name='videos', on_delete=models.CASCADE)
    video = models.FileField(_('post video'), null=False, blank=False, upload_to=get_post_video_file_path)


class PostAudio(models.Model):
    """
    This model will store all the audio of a post. Each post can have multiple audio.
    """
    post = models.ForeignKey(Post, related_name='audio', on_delete=models.CASCADE)
    audio = models.FileField(_('post audio'), null=False, blank=False, upload_to=get_post_audio_file_path)


class PostDocument(models.Model):
    """
    This model will store all the document of a post. Each post can have multiple document.
    """
    post = models.ForeignKey(Post, related_name='document', on_delete=models.CASCADE)
    document = models.FileField(_('post document'), null=False, blank=False, upload_to=get_post_document_file_path)


class PostAttachment(models.Model):
    """
    This model will store all the attachments of a post. Each post can have multiple attachments.
    """
    post = models.ForeignKey(Post, related_name='attachment', on_delete=models.CASCADE)
    attachment = models.FileField(_('post attachment'), null=False, blank=False,
                                  upload_to=get_post_attachment_file_path)


class Poll(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, primary_key=True)
    question = models.CharField(max_length=255)

    def __str__(self):
        return self.question


class PollChoice(models.Model):
    poll = models.ForeignKey(Poll, related_name='choices', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)

    def __str__(self):
        return self.choice_text


class PollVote(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.ForeignKey(PollChoice, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'poll')


class FavoritePost(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='favorite_post', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='favorite_post', on_delete=models.CASCADE)

    created_at = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')
