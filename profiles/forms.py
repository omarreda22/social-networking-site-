from django import forms
from django.utils.text import slugify
from django.utils import timezone
from django.core.exceptions import ValidationError


from accounts.models import NewUser
from .models import Profile


RANGE_YEARS = [x for x in range(1950, 2023)]
RANGE_YEARS.reverse()


class UpdateProfileForm(forms.ModelForm):
    date_of_birth = forms.CharField(
        widget=forms.SelectDateWidget(years=RANGE_YEARS),
    )

    class Meta:
        model = NewUser
        fields = [
            # 'email',
            'username',
            'first_name',
            'last_name',
            'country',
            'gender',
            'date_of_birth',
        ]

    # def clean_username(self):
    #     users = NewUser.objects.all()
    #     username = self.cleaned_data.get('username')
    #     print('omar')
    #     print(users)
    #     if username not in users:
    #         print('omar')
    #         raise ValidationError("Don't use this shit word")
    #     return username

    def __init__(self, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class UpdateBio(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio']

    def __init__(self, *args, **kwargs):
        super(UpdateBio, self).__init__(*args, **kwargs)

        self.fields['bio'].widget.attrs['class'] = 'form-control'


class UpdateImage(forms.ModelForm):
    # avatar = forms.ImageField()
    avatar = forms.ImageField(widget=forms.FileInput)

    class Meta:
        model = Profile
        fields = ['avatar']

    def __init__(self, *args, **kwargs):
        super(UpdateImage, self).__init__(*args, **kwargs)

        self.fields['avatar'].widget.attrs['class'] = 'form-control'
