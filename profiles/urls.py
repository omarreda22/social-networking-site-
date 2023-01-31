from django.urls import path
from . import views


app_name = 'profiles'

urlpatterns = [
    path('<str:slug>/', views.user_profile, name='profile'),
    path('<slug:slug>/update_bio', views.update_bio, name='edit_bio'),
    path('<slug:slug>/update_image', views.update_image, name='edit_image'),
    path('update_post/<int:post_id>/', views.update_post, name='update_post'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
]
