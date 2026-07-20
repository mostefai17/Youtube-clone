from django.urls import path
from . import views


urlpatterns = [
    path('', views.video_list, name='video_list'),
    path('upload/', views.video_upload_page, name='video_upload'), # GET - show form
    path('upload/submit/', views.video_upload, name='upload_submit'), # POST - handle submission
    path('<int:video_id>/', views.video_detail, name='video_detail')
]
