from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import Video
from .forms import VideoForm
from .imagekit_client import upload_video, upload_thumbnail


# Displaying video lists
def video_list(request):

    videos = Video.objects.all()
    return render(request, "videos/list.html", {"videos": videos})


# Writing Detail view
def video_detail(request, video_id):
    video = get_object_or_404(Video.objects.select_related('user'), id=video_id)
    return render(request, "videos/detail.html", {"video": video})

# Fixed decorators: Removed parentheses to prevent TypeErrors
@login_required
@require_POST
def video_upload(request):
    # Fixed form reference: Using imported VideoForm instead of VideoUploadForm
    form = VideoForm(request.POST, request.FILES)
    if form.is_valid():
        video_file = form.cleaned_data['video_file']
        custom_thumbnail = request.POST.get('thumbnail_url', '')

        try:
            # Fixed keyword argument typo: file_Data -> file_data
            result = upload_video(
                file_data=video_file.read(),
                file_name=video_file.name,
            )

            thumbnail_url = ''
            if custom_thumbnail and custom_thumbnail.startswith('data:image'):
                try:
                    base_name = video_file.name.rsplit(".", 1)[0]
                    thumb_result = upload_thumbnail(
                        file_data=custom_thumbnail,
                        file_name=f"{base_name}_thumbnail.jpg",
                    )
                    thumbnail_url = thumb_result['url']
                except Exception as e:
                    print(f"Error while loading thumbnail: {e}")
                    pass

            video = Video.objects.create(
                user=request.user,
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                file_id=result['file_id'],
                video_url=result['url'],
                thumbnail_url=thumbnail_url,
            )

            return JsonResponse({
                'success': True,
                'video_id': video.id,
                'message': 'Video uploaded successfully'
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': f"ImageKit Upload error: {str(e)}"}, status=500)

    errors = []
    for field, field_errors in form.errors.items():
        for error in field_errors:
            errors.append(f"{field}: {error}" if field != '__all__' else error)

    return JsonResponse({'success': False, 'error': "; ".join(errors)}, status=400)

@login_required
def video_upload_page(request):
    # Fixed dictionary syntax: Added quotes around the "form" key
    return render(request, "videos/upload.html", {"form": VideoForm()})