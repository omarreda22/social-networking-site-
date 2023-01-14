from django import forms

from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class CommentPostForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        labels = {
            'body': 'Content',
        }

    def __init__(self, *args, **kwargs):
        super(CommentPostForm, self).__init__(*args, **kwargs)

        self.fields['body'].widget.attrs['class'] = 'form-control'
