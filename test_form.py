import os
import sys
import django

sys.path.append(os.path.join(os.getcwd(), 'youtube'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'youtube_clone.settings')
django.setup()

from accounts import CustomUserCreationForm
form = CustomUserCreationForm()
print(form)
