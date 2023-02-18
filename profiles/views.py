from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from django.http import JsonResponse

from .models import Profile, Relationship
from .forms import UpdateProfileForm, UpdateBio, UpdateImage
from posts.forms import CommentPostForm, PostForm
from posts.models import Post


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def user_profile(request, slug):
    profile = Profile.objects.get(slug=slug)

    if request.user.username == profile.slug:
        InfoForm = UpdateProfileForm(
            request.POST or None, instance=profile.user)
        data = {}
        if is_ajax(request=request):
            if InfoForm.errors:
                data['infoError'] = InfoForm.errors
                return JsonResponse(data)

            if InfoForm.is_valid():
                username = request.POST.get('username')
                InfoForm.username = slugify(username)
                InfoForm.save()
                profile.slug = slugify(InfoForm.username)
                profile.save()
                data['infoError'] = InfoForm.errors
                data['username'] = InfoForm.cleaned_data.get('username')
                data['first_name'] = InfoForm.cleaned_data.get('first_name')
                data['last_name'] = InfoForm.cleaned_data.get('last_name')
                data['country'] = InfoForm.cleaned_data.get('country')
                data['gender'] = InfoForm.cleaned_data.get('gender')
                data['date'] = InfoForm.cleaned_data.get(
                    'date_of_birth')
                return JsonResponse(data)

        bio_form = UpdateBio(request.POST or None, instance=profile)

        avatar = UpdateImage(instance=profile)
        comment_form = CommentPostForm()

        post_form = PostForm()


        friends = profile.friends.all().order_by("?")[:5]
        friends_count = profile.friends.count()

        # me = request.user.profile
        friend_requests_count = Relationship.objects.friend_requests(me=profile).count()

        template_name = 'myprofile.html'
        context = {
            'profile': profile,
            'form': InfoForm,
            'bio_form': bio_form,
            'image_form': avatar,
            'comment_form': comment_form,
            'post_form': post_form,
            'friends': friends,
            'friends_count':friends_count,
            'friend_requests_count': friend_requests_count,
        }
        return render(request, template_name, context)

    template_name = 'profile.html'
    context = {
        'profile': profile,
    }
    return render(request, template_name, context)


def update_bio(request, slug):
    profile = Profile.objects.get(slug=slug)
    BioForm = UpdateBio(request.POST or None, instance=profile)
    data = {}
    if is_ajax(request=request):
        if BioForm.is_valid():
            BioForm.save()
            data['bio'] = BioForm.cleaned_data.get('bio')
            return JsonResponse(data)


def update_image(request, slug):
    profile = Profile.objects.get(slug=slug)
    avatarForm = UpdateImage(request.POST or None,
                             request.FILES or None, instance=profile)
    data = {}
    if is_ajax(request=request):
        if avatarForm.is_valid():
            avatarForm.save()
            data['status'] = 'ok'
            return JsonResponse(data)


def update_post(request, post_id):
    form = PostForm(request.POST or None, request.FILES or None)
    post = Post.objects.get(id=post_id)
    data = {}
    if is_ajax(request=request):
        if form.is_valid():
            content = form.cleaned_data.get('content')
            image = form.cleaned_data.get('image')
            if image != 'default/no-image.jpg':
                post.image = image
                data['image'] = f'/media/posts/{str(image)}'
            else:
                data['image'] = post.image.url

            post.content = content
            post.save()
            data['content'] = content
            return JsonResponse(data)


def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return JsonResponse({'status': 'Ok'})


def people_you_may_know(request, slug):
    user = request.user
    profiles = Profile.objects.all()



    template_name = 'nav_buttons/people_you_may_know.html'
    context = {
        'profiles': profiles,
    }
    return render(request, template_name, context)


def my_friends(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    my_friends = profile.friends.all()
    friends_count = my_friends.count()

    template_name = 'nav_buttons/my_friends.html'
    context = {
        'my_friends': my_friends,
        'friends_count': friends_count,
    }
    return render(request, template_name, context)


##### Some logic
def unfriend(request, myfriend):
    if is_ajax(request=request):
        user = Profile.objects.get(slug=myfriend)
        me = request.user.profile

        remove_relationship = Relationship.objects.unfriend(me, user)
        remove_relationship.status = Relationship.STATUS_CHOICES.REMOVE
        remove_relationship.save()
        data = {'ok': myfriend}
        # friend = 
        return JsonResponse(data)

    data = {'ok': 'error'}
    return JsonResponse(data)


# Friend Requests
def friend_request(request):
    user = request.user
    user_profile = user.profile
    requests = Relationship.objects.friend_requests(me=user_profile).only('sender')
    requests_count = requests.count()
    
    template_name = 'nav_buttons/friend_requests.html'
    context = {
        'requests': requests,
        'count':requests_count,
    }
    return render(request, template_name, context)


def new_status(request, rId):
    status = request.POST['status']
    user = request.user.profile
    relationship = Relationship.objects.get(id=rId, receiver=user)

    if status == "Accept":
        relationship.status = Relationship.STATUS_CHOICES.ACCEPT
    
    if status == "Remove":
        relationship.status = Relationship.STATUS_CHOICES.REMOVE
    
    relationship.save()
    
    data = {'new_relationship': relationship.status,}
    return JsonResponse(data)