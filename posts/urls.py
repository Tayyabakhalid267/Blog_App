from django.urls import path
from .views import home_view, signup_view, edit_post, delete_post, about_view, contact_view, help_view

urlpatterns = [
    path('', home_view, name='home'),
    path('signup/', signup_view, name='signup'),
    path('post/<int:pk>/edit/', edit_post, name='post_edit'),
    path('post/<int:pk>/delete/', delete_post, name='post_delete'),
    path('about/', about_view, name='about'),
    path('contact/', contact_view, name='contact'),
    path('help/', help_view, name='help'),
]
