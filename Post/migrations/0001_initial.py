# Generated by Django 5.0 on 2023-12-09 11:09

import Bargad.utils
import django.db.models.deletion
import functools
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FavoritePost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created')),
            ],
        ),
        migrations.CreateModel(
            name='LikeDislikeComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.SmallIntegerField(choices=[(1, 'Like'), (-1, 'Dislike')])),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='timestamp')),
            ],
        ),
        migrations.CreateModel(
            name='LikeDislikePost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.SmallIntegerField(choices=[(1, 'Like'), (-1, 'Dislike')])),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='timestamp')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('caption', models.CharField(max_length=120, verbose_name='caption')),
                ('description', models.CharField(blank=True, max_length=520, null=True, verbose_name='description')),
                ('share_count', models.PositiveIntegerField(default=0, verbose_name='No of times post has been shared')),
                ('is_edited', models.BooleanField(default=False, verbose_name='is edited')),
                ('edit_count', models.PositiveIntegerField(default=0, verbose_name='No of times post has been edited')),
                ('like_count', models.PositiveIntegerField(default=0, verbose_name='No of likes')),
                ('comment_count', models.PositiveIntegerField(default=0, verbose_name='No of comments')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated')),
            ],
        ),
        migrations.CreateModel(
            name='PollChoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='PollVote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='PostAttachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attachment', models.FileField(upload_to=functools.partial(Bargad.utils.get_image_file_path, *('post_attachments',), **{}), verbose_name='post attachment')),
            ],
        ),
        migrations.CreateModel(
            name='PostAudio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('audio', models.FileField(upload_to=functools.partial(Bargad.utils.get_image_file_path, *('post_audios',), **{}), verbose_name='post audio')),
            ],
        ),
        migrations.CreateModel(
            name='PostDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.FileField(upload_to=functools.partial(Bargad.utils.get_image_file_path, *('post_documents',), **{}), verbose_name='post document')),
            ],
        ),
        migrations.CreateModel(
            name='PostGifs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gif', models.FileField(upload_to=functools.partial(Bargad.utils.get_image_file_path, *('post_gifs',), **{}), verbose_name='post gif')),
            ],
        ),
        migrations.CreateModel(
            name='PostImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=functools.partial(Bargad.utils.get_image_file_path, *('post_images',), **{}), verbose_name='post image')),
            ],
        ),
        migrations.CreateModel(
            name='PostTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(db_index=True, max_length=120, unique=True, verbose_name='tag')),
            ],
        ),
        migrations.CreateModel(
            name='PostVideos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.FileField(upload_to=functools.partial(Bargad.utils.get_image_file_path, *('post_videos',), **{}), verbose_name='post video')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('text', models.CharField(blank=True, max_length=120, null=True, verbose_name='caption')),
                ('image', models.ImageField(blank=True, null=True, upload_to=functools.partial(Bargad.utils.get_image_file_path, *('comment_images',), **{}), verbose_name='comment image')),
                ('gif', models.FileField(blank=True, null=True, upload_to=functools.partial(Bargad.utils.get_image_file_path, *('comment_gifs',), **{}), verbose_name='comment gif')),
                ('video', models.FileField(blank=True, null=True, upload_to=functools.partial(Bargad.utils.get_image_file_path, *('comment_videos',), **{}), verbose_name='comment video')),
                ('audio', models.FileField(blank=True, null=True, upload_to=functools.partial(Bargad.utils.get_image_file_path, *('comment_audios',), **{}), verbose_name='comment audio')),
                ('document', models.FileField(blank=True, null=True, upload_to=functools.partial(Bargad.utils.get_image_file_path, *('comment_documents',), **{}), verbose_name='comment document')),
                ('attachment', models.FileField(blank=True, null=True, upload_to=functools.partial(Bargad.utils.get_image_file_path, *('comment_attachments',), **{}), verbose_name='comment attachment')),
                ('is_edited', models.BooleanField(default=False, verbose_name='is edited')),
                ('edit_count', models.PositiveIntegerField(default=0, verbose_name='No of times comment has been edited')),
                ('like_count', models.PositiveIntegerField(default=0, verbose_name='No of likes')),
                ('comment_count', models.PositiveIntegerField(default=0, verbose_name='No of comments')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated')),
                ('original_comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='edited_comment', to='Post.comment')),
            ],
        ),
    ]
