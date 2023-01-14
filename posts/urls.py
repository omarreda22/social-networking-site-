from django.urls import path

from . import views

app_name = 'posts'


urlpatterns = [
    path('', views.posts_main, name='main'),
    path('<int:id>/like_unlike', views.posts_like_unlike, name='like_unlike'),
    path('new_post/', views.new_post, name='new_post'),
    path('new_comment/<int:post_id>', views.add_comment, name='new_post'),
    path('update_comment/<int:comment_id>',
         views.update_comment, name='comment_id'),
    path('delete_comment/<int:comment_id>',
         views.delete_comment, name='delete_comment'),
]
