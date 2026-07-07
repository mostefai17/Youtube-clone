from django import forms

class VideoForm(forms.Form):
    title = forms.CharField(
        max_length=200,
        widget = forms.TextInput(
            attrs={'class':'form-input'
                   ,'placeholder':'Please Enter a Video Title'}
        ),

    )

    description = forms.CharField(
        required=False,
        widget = forms.Textarea(
            attrs={'class':'form-input'
                   ,'placeholder':'Please Enter a Video Description'
                   ,'rows' : 3}
        )
    )

    video_file = forms.FileField(
        widget = forms.FileInput(
            attrs={'class':'form-input',
                   'accept': 'video/*'}
        )
    )

    def clean_video_file(self):
        video = self.cleaned_data.get('video_file')
        if video:
            if video.size > 500 * 1024 * 1024:
                raise forms.ValidationError('Video file size cannot be more than 500MB')

            allowed_type = ["video/mp4", "video/x-m4v", "video/quicktime"]
            if video.content_type not in allowed_type:
                raise forms.ValidationError('This video type is not allowed')

        return video


