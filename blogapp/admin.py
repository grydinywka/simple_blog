from django.contrib import admin
from .models import UserOwner, Blog, Post


admin.site.register(UserOwner)
admin.site.register(Blog)
admin.site.register(Post)


