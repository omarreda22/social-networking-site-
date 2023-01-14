from django.shortcuts import render
from django.http import HttpResponse, JsonResponse


from .models import Post, Comment
from profiles.models import Profile
from .forms import PostForm, CommentPostForm


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


# must be authenticated ########################
def posts_main(request):
    posts = Post.objects.all()
    user = request.user
    form = PostForm()
    comment_form = CommentPostForm()

    template_name = 'posts_main.html'
    context = {
        'posts': posts,
        'form': form,
        'user': user,
        'comment_form': comment_form,
    }

    return render(request, template_name, context)


def posts_like_unlike(request, id):
    post = Post.objects.get(id=id)
    user = request.user
    profile = Profile.objects.get(user=user)
    if profile in post.likes.all():
        post.likes.remove(profile)
    else:
        post.likes.add(profile)
    post.save()

    data = {}
    # if is_ajax(request=request):
    #     data['value'] = post.content
    #     return JsonResponse(data)
    return JsonResponse(data)


def new_post(request):
    form = PostForm(request.POST or None, request.FILES or None)
    profile = Profile.objects.get(user=request.user)
    data = {}
    if is_ajax(request=request):
        if form.is_valid():
            post = form.save(commit=False)
            post.user = profile
            post.save()
            data['user_image'] = profile.avatar.url
            data['user_username'] = profile.user.username
            data['image'] = post.image.url
            data['content'] = post.content
            data['post_id'] = post.id

            return JsonResponse(data)
    return JsonResponse(data)


def add_comment(request, post_id):
    form = CommentPostForm(request.POST or None)
    post = Post.objects.get(id=post_id)
    user = request.user.profile

    data = {}
    if is_ajax(request=request):
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.user = user
            new_comment.save()

            data['body'] = new_comment.body
            data['avatar'] = user.avatar.url
            data['user'] = user.user.username
            return JsonResponse(data)
    return JsonResponse({"some erorrs": form.data})


def update_comment(request, comment_id):
    form = CommentPostForm(request.POST or None)
    comment = Comment.objects.get(id=comment_id)
    data = {}
    if is_ajax(request=request):
        if form.is_valid():
            body = form.cleaned_data.get('body')
            comment.body = body
            comment.save()
            data['body'] = body
            return JsonResponse(data)

    return JsonResponse({"some erorrs": form.data})


def delete_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
    return JsonResponse({'data': 'ok post deleted'})
