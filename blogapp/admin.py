from django.contrib import admin
from django.forms import ModelForm, ValidationError
from .models import UserOwner, Blog, Post


class BlogFormAdmin(ModelForm):
    def clean_posts(self):
        """Check if blog's posts belong to single owner"""
        users_id = {post.user.id for post in self.cleaned_data['posts'].all()}
        if len(users_id) != 1:
            raise ValidationError("The blog do not allow have posts from different users")
        if hasattr(self.instance, 'userowner') == False:
            raise ValidationError("For adding posts blog must belong to one user.")
        if not self.instance.userowner.id in users_id:
            raise ValidationError("owner of the blog did not write the post")
        return self.cleaned_data['posts']


class BlogAdmin(admin.ModelAdmin):
    form = BlogFormAdmin

admin.site.register(UserOwner)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Post)


