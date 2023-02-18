from django.urls import path
from . import views


app_name = 'profiles'

urlpatterns = [
    path('<str:slug>/', views.user_profile, name='profile'),
    path('<slug:slug>/update_bio', views.update_bio, name='edit_bio'),
    path('<slug:slug>/update_image', views.update_image, name='edit_image'),
    
    # Update Posts
    path('update_post/<int:post_id>/', views.update_post, name='update_post'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),

    # Nav Buttons 
    path("<str:slug>/people_you_may_know/", views.people_you_may_know, name="people_you_may_know"),

    path("myfriends/all", views.my_friends, name="my_friends"),
    path("friend/delete/<str:myfriend>", views.unfriend, name="unfriend"),

    path("friend_requests/all", views.friend_request, name="friend_requests"),
    path("<int:rId>/friend_requests/new_status/", views.new_status, name='new_status'),
    
]
