from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class Blog(models.Model):
    writer = models.ForeignKey(User, editable =False, null=True, blank=True, on_delete=models.SET_NULL,)
    title=models.CharField(max_length=200)
    place_thing = (('서울', '서울'), ('경기', '경기'), ('강원', '강원'),)
    place = models.CharField(max_length=3, choices=place_thing, default='서울',)
    type_thing = (('카페', '카페'), ('식당', '식당'), ('산책', '산책'),)
    placetype = models.CharField(max_length=3, choices=type_thing, default='카페',)
    date = models.DateTimeField(auto_now_add=True)
    explain = models.TextField(default='')
    image = models.ImageField(upload_to='images/', blank=True)
    menupicture = models.ImageField(upload_to='images/', blank=True)
    menutext = models.TextField(default='')

    def __str__(self):
        return self.title
    
    def summary(self):
        return self.content[:100]

class BlogLike(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Comment(models.Model):
    post_key = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True, related_name='comments')
    comment_date = models.DateTimeField(auto_now_add=True)
    comment_contents = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.comment_contents
        