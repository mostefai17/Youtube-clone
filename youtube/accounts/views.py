from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm

# Create your views here.

# Writing custom register view

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = '/'
    template_name = 'accounts/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return redirect('/')


@login_required
def profile_view(request):
    videos = request.user.videos.all().order_by('-created_at')
    return render(request, 'accounts/profile.html', {'videos': videos})
