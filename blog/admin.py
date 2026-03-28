from django.contrib import admin

from .models import Post, Comment, Like, Story, Profile

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Story)
admin.site.register(Profile)

