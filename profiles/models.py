from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, post_save


User = settings.AUTH_USER_MODEL


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(null=True, blank=True)
    bio = models.TextField(
        max_length=500, default='no bio...', blank=True, null=True)
    avatar = models.ImageField(
        upload_to='users_avatar', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    friends = models.ManyToManyField(
        User, blank=True, related_name='friends')

    def __str__(self):
        return self.user.username

    def get_posts_count(self):
        return self.post_set.all().count()

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = self.user.username
        super().save(*args, **kwargs)


def avatar_signal(sender, instance, *args, **kwargs):
    if instance.avatar == '' or not instance.avatar:
        if instance.user.gender == instance.user.GENDER.MALE:
            instance.avatar = './default/avatar_male.png'
        if instance.user.gender == instance.user.GENDER.FEMALE:
            instance.avatar = './default/avatar_female.png'


pre_save.connect(avatar_signal, sender=Profile)


# # # Create Profile when user created
def create_profile_signal(sender, created, instance, *args, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        pass


post_save.connect(create_profile_signal, sender=User)

######################################################################################
######################################################################################

# Relationship.objects.invation_received(myprofile)
# Custom Query Set


class RelationshipQuerySet(models.QuerySet):
    def send_add(self, receiver):
        qs = self.filter(receiver=receiver,
                         status=Relationship.STATUS_CHOICES.SEND)
        return qs


class RelationshipManager(models.Manager):
    def get_queryset(self):
        return RelationshipQuerySet(self.model, using=self.db)

    def adds_receiver(self, receiver):
        return self.get_queryset().send_add(receiver)


class Relationship(models.Model):
    class STATUS_CHOICES(models.TextChoices):
        SEND = 'SEND', 'Send'
        ACCEPT = 'ACC', 'Accept'
        CANCEL = 'CAN', 'Cancel'

    sender = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=6, choices=STATUS_CHOICES.choices)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = RelationshipManager()

    def __str__(self):
        return f'{self.sender} to {self.receiver}'

    @property
    def is_accepted(self):
        return self.status == self.STATUS_CHOICES.ACCEPT

    def save(self, *args, **kwargs):
        """ 
        if receiver accept add, will be added in friends list
        """
        sender = self.sender
        rec = self.receiver
        if self.is_accepted:
            sender.friends.add(rec.user)
            rec.friends.add(sender.user)
        super().save(*args, **kwargs)
