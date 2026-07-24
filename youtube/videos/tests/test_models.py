from django.test import TestCase
from django.contrib.auth.models import User
from youtube.videos.models import Video, VideoLike


class VideoModelTestCase(TestCase):
    """Tests for the Video model"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.video = Video.objects.create(
            user=self.user,
            title='Test Video',
            description='Test Description',
            file_id='test_file_123',
            video_url='https://example.com/video.mp4',
            thumbnail_url='https://example.com/thumb.jpg'
        )

    def test_video_creation(self):
        """Test that a video can be created with required fields"""
        self.assertEqual(self.video.title, 'Test Video')
        self.assertEqual(self.video.description, 'Test Description')
        self.assertEqual(self.video.user, self.user)
        self.assertEqual(self.video.file_id, 'test_file_123')

    def test_video_default_values(self):
        """Test that video default values are set correctly"""
        self.assertEqual(self.video.views, 0)
        self.assertEqual(self.video.likes, 0)
        self.assertEqual(self.video.dislikes, 0)

    def test_video_string_representation(self):
        """Test video string representation"""
        self.assertEqual(str(self.video), 'Test Video')

    def test_video_ordering(self):
        """Test that videos are ordered by creation date descending"""
        video2 = Video.objects.create(
            user=self.user,
            title='Second Video',
            file_id='test_file_456',
            video_url='https://example.com/video2.mp4'
        )
        videos = Video.objects.all()
        self.assertEqual(videos[0], video2)
        self.assertEqual(videos[1], self.video)

    def test_video_with_empty_thumbnail(self):
        """Test video with empty thumbnail URL"""
        video = Video.objects.create(
            user=self.user,
            title='No Thumbnail Video',
            file_id='test_file_789',
            video_url='https://example.com/video3.mp4',
            thumbnail_url=''
        )
        self.assertEqual(video.thumbnail_url, '')

    def test_display_thumbnail_url_with_uploaded_thumbnail(self):
        """Test display_thumbnail_url property when custom thumbnail is uploaded"""
        self.video.thumbnail_url = 'https://example.com/thumbnails/custom.jpg'
        self.assertEqual(
            self.video.display_thumbnail_url,
            'https://example.com/thumbnails/custom.jpg'
        )

    def test_display_thumbnail_url_without_custom_thumbnail(self):
        """Test display_thumbnail_url falls back to generated when no custom"""
        self.video.thumbnail_url = ''
        result = self.video.display_thumbnail_url
        self.assertEqual(result, self.video.generated_thumbnail_url)

    def test_generated_thumbnail_url(self):
        """Test generated thumbnail URL from video URL"""
        expected_url = 'https://example.com/video.mp4/ik-thumbnail.jpg'
        self.assertEqual(self.video.generated_thumbnail_url, expected_url)

    def test_generated_thumbnail_url_empty_video_url(self):
        """Test generated thumbnail returns empty string when video_url is empty"""
        self.video.video_url = ''
        self.assertEqual(self.video.generated_thumbnail_url, '')

    def test_streaming_video_url(self):
        """Test streaming video URL property"""
        expected_url = 'https://example.com/video.mp4?ik-master.m3u8'
        self.assertEqual(self.video.streaming_video_url, expected_url)

    def test_streaming_video_url_empty_video_url(self):
        """Test streaming video URL returns empty string when video_url is empty"""
        self.video.video_url = ''
        self.assertEqual(self.video.streaming_video_url, '')

    def test_optimized_video_url_without_query_params(self):
        """Test optimized video URL when video URL has no query params"""
        expected_url = 'https://example.com/video.mp4?tr=q-80,f-auto'
        self.assertEqual(self.video.optimized_video_url, expected_url)

    def test_optimized_video_url_with_query_params(self):
        """Test optimized video URL when video URL already has query params"""
        self.video.video_url = 'https://example.com/video.mp4?param=value'
        expected_url = 'https://example.com/video.mp4?param=value&tr=q-80,f-auto'
        self.assertEqual(self.video.optimized_video_url, expected_url)

    def test_optimized_video_url_empty_video_url(self):
        """Test optimized video URL returns empty string when video_url is empty"""
        self.video.video_url = ''
        self.assertEqual(self.video.optimized_video_url, '')

    def test_video_user_relationship(self):
        """Test that videos are related to users"""
        self.assertEqual(self.video.user.username, 'testuser')
        self.assertIn(self.video, self.user.videos.all())

    def test_video_cascade_delete(self):
        """Test that videos are deleted when user is deleted"""
        video_id = self.video.id
        self.user.delete()
        self.assertFalse(Video.objects.filter(id=video_id).exists())


class VideoLikeModelTestCase(TestCase):
    """Tests for the VideoLike model"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.video = Video.objects.create(
            user=self.user,
            title='Test Video',
            file_id='test_file_123',
            video_url='https://example.com/video.mp4'
        )

    def test_like_creation(self):
        """Test that a like can be created"""
        like = VideoLike.objects.create(
            user=self.user,
            video=self.video,
            value=VideoLike.LIKE
        )
        self.assertEqual(like.user, self.user)
        self.assertEqual(like.video, self.video)
        self.assertEqual(like.value, VideoLike.LIKE)

    def test_dislike_creation(self):
        """Test that a dislike can be created"""
        dislike = VideoLike.objects.create(
            user=self.user,
            video=self.video,
            value=VideoLike.DISLIKE
        )
        self.assertEqual(dislike.value, VideoLike.DISLIKE)

    def test_like_string_representation_like(self):
        """Test string representation of a like"""
        like = VideoLike.objects.create(
            user=self.user,
            video=self.video,
            value=VideoLike.LIKE
        )
        self.assertEqual(str(like), f'{self.user.username} likes {self.video.title}')

    def test_like_string_representation_dislike(self):
        """Test string representation of a dislike"""
        dislike = VideoLike.objects.create(
            user=self.user,
            video=self.video,
            value=VideoLike.DISLIKE
        )
        self.assertEqual(str(dislike), f'{self.user.username} dislikes {self.video.title}')

    def test_unique_together_constraint(self):
        """Test that a user can only like/dislike a video once"""
        VideoLike.objects.create(
            user=self.user,
            video=self.video,
            value=VideoLike.LIKE
        )
        with self.assertRaises(Exception):
            VideoLike.objects.create(
                user=self.user,
                video=self.video,
                value=VideoLike.LIKE
            )

    def test_different_users_can_like_same_video(self):
        """Test that different users can like the same video"""
        user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )
        like1 = VideoLike.objects.create(
            user=self.user,
            video=self.video,
            value=VideoLike.LIKE
        )
        like2 = VideoLike.objects.create(
            user=user2,
            video=self.video,
            value=VideoLike.LIKE
        )
        self.assertEqual(VideoLike.objects.filter(video=self.video).count(), 2)

    def test_same_user_can_like_different_videos(self):
        """Test that same user can like different videos"""
        video2 = Video.objects.create(
            user=self.user,
            title='Second Video',
            file_id='test_file_456',
            video_url='https://example.com/video2.mp4'
        )
        like1 = VideoLike.objects.create(
            user=self.user,
            video=self.video,
            value=VideoLike.LIKE
        )
        like2 = VideoLike.objects.create(
            user=self.user,
            video=video2,
            value=VideoLike.LIKE
        )
        self.assertEqual(VideoLike.objects.filter(user=self.user).count(), 2)

    def test_like_cascade_delete_on_user(self):
        """Test that likes are deleted when user is deleted"""
        VideoLike.objects.create(
            user=self.user,
            video=self.video,
            value=VideoLike.LIKE
        )
        self.user.delete()
        self.assertFalse(VideoLike.objects.filter(video=self.video).exists())

    def test_like_cascade_delete_on_video(self):
        """Test that likes are deleted when video is deleted"""
        like = VideoLike.objects.create(
            user=self.user,
            video=self.video,
            value=VideoLike.LIKE
        )
        like_id = like.id
        self.video.delete()
        self.assertFalse(VideoLike.objects.filter(id=like_id).exists())
