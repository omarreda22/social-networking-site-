from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, post_save


User = settings.AUTH_USER_MODEL


class Profile(models.Model):
    class GENDER(models.TextChoices):
        MALE = 'MALE', 'Male'
        FEMALE = 'FEMALE', 'Female'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=125)
    last_name = models.CharField(max_length=125)
    slug = models.SlugField(null=True, blank=True)
    bio = models.TextField(
        max_length=500, default='no bio...', blank=True, null=True)
    email = models.EmailField()
    avatar = models.ImageField(
        upload_to='users_avatar', blank=True, null=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER.choices)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    friends = models.ManyToManyField(
        User, blank=True, null=True, related_name='friends')

    def __str__(self):
        return self.user.username

    # set Slug
    # set Image
    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = self.user.username
        super().save(*args, **kwargs)


def avatar_singnal(sender, instance, *args, **kwargs):
    if instance.avatar == '' or not instance.avatar:
        if instance.gender == instance.GENDER.MALE:
            instance.avatar = './default/avatar_male.png'
        if instance.gender == instance.GENDER.FEMALE:
            instance.avatar = './default/avatar_female.png'


pre_save.connect(avatar_singnal, sender=Profile)
