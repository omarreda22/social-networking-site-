from django.shortcuts import render, redirect
from django.utils.text import slugify
from django.http import JsonResponse

from .models import Profile
from .forms import UpdateProfileForm, UpdateBio, UpdateImage


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

        template_name = 'myprofile.html'
        context = {
            'profile': profile,
            'form': InfoForm,
            'bio_form': bio_form,
            'image_form': avatar,
        }
        return render(request, template_name, context)

    template_name = 'profile.html'
    context = {
        'profile': profile,
    }
    return render(request, template_name, context)


# def update_bio(request, slug):
#     profile = Profile.objects.get(slug=slug)
#     bio_form = UpdateBio(request.POST, instance=profile)
#     if bio_form.is_valid():
#         bio_form = bio_form.save(commit=False)
#         bio_form.save()
#         return redirect(f'/myprofile/{profile.slug}')


# def update_image(request, slug):
#     profile = Profile.objects.get(slug=slug)
#     image_form = UpdateImage(
#         request.POST, request.FILES or None, instance=profile)
#     if image_form.is_valid():
#         image_form.save()
#         return redirect(f'/myprofile/{profile.slug}')
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
