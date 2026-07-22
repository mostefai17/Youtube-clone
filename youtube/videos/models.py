from django.db import models
from django.contrib.auth.models import User
from .imagekit_client import get_optimized_video_url, get_streaming_video_url, get_thumbnail_url
# Create your models here.

class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    file_id = models.CharField(max_length=200)
    video_url = models.URLField(max_length=200)
    thumbnail_url = models.URLField(max_length=200, blank=True)

    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def display_thumbnail_url(self):
        if self.thumbnail_url and "/thumbnails/" in self.thumbnail_url:
            return self.thumbnail_url
        return self.generated_thumbnail_url # for more information revise the imagekit thumbnail documentation

    @property
    def generated_thumbnail_url(self):
        if not self.video_url:
            return ""
        return get_thumbnail_url(self.video_url)

    @property
    def streaming_video_url(self):
        if not self.video_url:
            return ""
        return get_streaming_video_url(self.video_url)
    
    @property
    def optimized_video_url(self):
        if not self.video_url:
            return ""
        return get_optimized_video_url(self.video_url)

class VideoLike(models.Model):
    LIKE = 1
    DISLIKE = -1
    LIKE_CHOICES = [
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='liked_by')
    value = models.SmallIntegerField(choices=LIKE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'video')  # Ensure a user can only like/dislike a video once


    def __str__(self):
        action = "likes" if self.value == self.LIKE else "dislikes"
        return f"{self.user.username} {action} {self.video.title}"