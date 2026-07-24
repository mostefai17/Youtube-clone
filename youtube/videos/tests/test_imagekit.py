from django.test import TestCase
from youtube.videos.imagekit_client import (
    get_optimized_video_url,
    get_streaming_video_url,
    get_thumbnail_url
)


class ImageKitUtilitiesTestCase(TestCase):
    """Tests for ImageKit utility functions"""

    def test_get_optimized_video_url_without_query_params(self):
        """Test optimized URL generation without existing query params"""
        base_url = 'https://example.com/video.mp4'
        result = get_optimized_video_url(base_url)
        self.assertEqual(result, 'https://example.com/video.mp4?tr=q-80,f-auto')

    def test_get_optimized_video_url_with_query_params(self):
        """Test optimized URL generation with existing query params"""
        base_url = 'https://example.com/video.mp4?param=value'
        result = get_optimized_video_url(base_url)
        self.assertEqual(result, 'https://example.com/video.mp4?param=value&tr=q-80,f-auto')

    def test_get_streaming_video_url(self):
        """Test streaming URL generation"""
        base_url = 'https://example.com/video.mp4'
        result = get_streaming_video_url(base_url)
        self.assertEqual(result, 'https://example.com/video.mp4?ik-master.m3u8')

    def test_get_streaming_video_url_with_query_params(self):
        """Test streaming URL with existing query params"""
        base_url = 'https://example.com/video.mp4?param=value'
        result = get_streaming_video_url(base_url)
        self.assertEqual(result, 'https://example.com/video.mp4?param=value?ik-master.m3u8')

    def test_get_thumbnail_url(self):
        """Test thumbnail URL generation"""
        base_url = 'https://example.com/video.mp4'
        result = get_thumbnail_url(base_url)
        self.assertEqual(result, 'https://example.com/video.mp4/ik-thumbnail.jpg')

    def test_get_thumbnail_url_custom_dimensions(self):
        """Test thumbnail URL generation with custom dimensions"""
        base_url = 'https://example.com/video.mp4'
        result = get_thumbnail_url(base_url, width=640, height=360)
        self.assertEqual(result, 'https://example.com/video.mp4/ik-thumbnail.jpg')

    def test_optimized_video_url_preserves_base(self):
        """Test that optimized URL preserves the base URL"""
        base_url = 'https://ik.imagekit.io/example/video.mp4'
        result = get_optimized_video_url(base_url)
        self.assertIn('https://ik.imagekit.io/example/video.mp4', result)
        self.assertIn('tr=q-80,f-auto', result)

    def test_streaming_video_url_preserves_base(self):
        """Test that streaming URL preserves the base URL"""
        base_url = 'https://ik.imagekit.io/example/video.mp4'
        result = get_streaming_video_url(base_url)
        self.assertIn('https://ik.imagekit.io/example/video.mp4', result)
        self.assertIn('ik-master.m3u8', result)

    def test_thumbnail_url_preserves_base(self):
        """Test that thumbnail URL preserves the base URL"""
        base_url = 'https://ik.imagekit.io/example/video.mp4'
        result = get_thumbnail_url(base_url)
        self.assertIn('https://ik.imagekit.io/example/video.mp4', result)
        self.assertIn('ik-thumbnail.jpg', result)

    def test_multiple_query_params_optimized(self):
        """Test optimized URL with multiple existing query params"""
        base_url = 'https://example.com/video.mp4?param1=value1&param2=value2'
        result = get_optimized_video_url(base_url)
        self.assertEqual(
            result,
            'https://example.com/video.mp4?param1=value1&param2=value2&tr=q-80,f-auto'
        )
