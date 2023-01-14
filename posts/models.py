from django.db import models
from django.utils import timezone

from profiles.models import Profile
from django.core.validators import FileExtensionValidator


class Post(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='posts', default="default/no-image.jpg", blank=True, validators=[
                              FileExtensionValidator(['png', 'jpg'])])
    likes = models.ManyToManyField(Profile, blank=True, related_name='likes')

    create = models.DateTimeField(auto_now=True)  # updated real
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:20]

    def num_likes(self):
        return self.likes.all().count()

    # num of counts
    def num_comments(self):
        return self.comment_set.all().count()

    def comments_before(self):
        users = []
        for comment in self.comment_set.all():
            users.append(comment.user)
        return users

    class Meta:
        ordering = ['-updated']

# Every comment has button updated


class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField(max_length=300)
    create = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {str(self.post)[:20]}'

    class Meta:
        ordering = ['-updated']


class Like(models.Model):
    class VALUE_CHOCIES(models.TextChoices):
        LIKE = 'like', 'Like'
        UNLIKE = 'unlike', 'unLike'

    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(max_length=9, choices=VALUE_CHOCIES.choices)
    create = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.post} - {self.user} - {self.value}"
