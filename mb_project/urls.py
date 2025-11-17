from django.contrib import admin
from django.urls import path, include
from posts.views import logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    # Custom logout view so we can guarantee a redirect to the login page
    path('accounts/logout/', logout_view, name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('posts.urls')),
]
