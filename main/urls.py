from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('chat.urls')),  # points to urls file in our `chat` app
    path('admin/', admin.site.urls),
]
