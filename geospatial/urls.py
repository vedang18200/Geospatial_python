from django.contrib import admin
from django.urls import path, include  # Include is used for app URLs

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),  # Ensure this points to your app's `urls.py`
]
