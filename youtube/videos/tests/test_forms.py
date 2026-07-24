from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from youtube.videos.forms import VideoForm


class VideoFormTestCase(TestCase):
    """Tests for the VideoForm"""

    def test_valid_video_form(self):
        """Test a valid video form"""
        video_file = SimpleUploadedFile(
            'test.mp4',
            b'file_content',
            content_type='video/mp4'
        )
        form_data = {
            'title': 'Test Video',
            'description': 'Test Description',
            'video_file': video_file
        }
        form = VideoForm(data=form_data, files={'video_file': video_file})
        self.assertTrue(form.is_valid())

    def test_video_form_title_required(self):
        """Test that title is required"""
        form_data = {
            'title': '',
            'description': 'Test Description'
        }
        form = VideoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_video_form_title_max_length(self):
        """Test title max length"""
        long_title = 'a' * 201
        form_data = {
            'title': long_title,
            'description': 'Test Description'
        }
        form = VideoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_video_form_description_optional(self):
        """Test that description is optional"""
        video_file = SimpleUploadedFile(
            'test.mp4',
            b'file_content',
            content_type='video/mp4'
        )
        form_data = {
            'title': 'Test Video',
            'description': '',
        }
        form = VideoForm(data=form_data, files={'video_file': video_file})
        # Description should be valid as empty
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data.get('description'), '')

    def test_video_form_video_file_required(self):
        """Test that video file is required"""
        form_data = {
            'title': 'Test Video',
            'description': 'Test Description',
        }
        form = VideoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('video_file', form.errors)

    def test_video_file_size_validation_valid(self):
        """Test video file size validation with valid size"""
        video_file = SimpleUploadedFile(
            'test.mp4',
            b'file_content' * 1000,
            content_type='video/mp4'
        )
        form_data = {
            'title': 'Test Video',
            'description': 'Test Description',
        }
        form = VideoForm(data=form_data, files={'video_file': video_file})
        self.assertTrue(form.is_valid())

    def test_video_file_size_validation_too_large(self):
        """Test video file size validation with too large file"""
        # Create a file larger than 500MB
        large_content = b'x' * (501 * 1024 * 1024)
        video_file = SimpleUploadedFile(
            'large.mp4',
            large_content,
            content_type='video/mp4'
        )
        form_data = {
            'title': 'Test Video',
            'description': 'Test Description',
        }
        form = VideoForm(data=form_data, files={'video_file': video_file})
        self.assertFalse(form.is_valid())
        self.assertIn('video_file', form.errors)
        self.assertIn('500MB', str(form.errors['video_file'][0]))

    def test_video_file_type_validation_mp4(self):
        """Test video file type validation with mp4"""
        video_file = SimpleUploadedFile(
            'test.mp4',
            b'file_content',
            content_type='video/mp4'
        )
        form_data = {
            'title': 'Test Video',
            'description': 'Test Description',
        }
        form = VideoForm(data=form_data, files={'video_file': video_file})
        self.assertTrue(form.is_valid())

    def test_video_file_type_validation_m4v(self):
        """Test video file type validation with m4v"""
        video_file = SimpleUploadedFile(
            'test.m4v',
            b'file_content',
            content_type='video/x-m4v'
        )
        form_data = {
            'title': 'Test Video',
            'description': 'Test Description',
        }
        form = VideoForm(data=form_data, files={'video_file': video_file})
        self.assertTrue(form.is_valid())

    def test_video_file_type_validation_quicktime(self):
        """Test video file type validation with quicktime"""
        video_file = SimpleUploadedFile(
            'test.mov',
            b'file_content',
            content_type='video/quicktime'
        )
        form_data = {
            'title': 'Test Video',
            'description': 'Test Description',
        }
        form = VideoForm(data=form_data, files={'video_file': video_file})
        self.assertTrue(form.is_valid())

    def test_video_file_type_validation_invalid(self):
        """Test video file type validation with invalid type"""
        video_file = SimpleUploadedFile(
            'test.txt',
            b'file_content',
            content_type='text/plain'
        )
        form_data = {
            'title': 'Test Video',
            'description': 'Test Description',
        }
        form = VideoForm(data=form_data, files={'video_file': video_file})
        self.assertFalse(form.is_valid())
        self.assertIn('video_file', form.errors)
        self.assertIn('not allowed', str(form.errors['video_file'][0]))

    def test_form_fields_attributes(self):
        """Test that form fields have correct attributes"""
        form = VideoForm()
        self.assertIn('form-input', str(form['title'].field.widget.attrs))
        self.assertIn('form-input', str(form['description'].field.widget.attrs))
        self.assertIn('form-input', str(form['video_file'].field.widget.attrs))
        self.assertIn('video/*', str(form['video_file'].field.widget.attrs))
