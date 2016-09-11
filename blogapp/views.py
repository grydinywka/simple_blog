from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.views.generic import UpdateView, CreateView
from django.contrib.auth.views import deprecate_current_app, _get_login_redirect_url
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from crispy_forms.bootstrap import FormActions
from django.views.generic import ListView,TemplateView,DetailView

from blogapp.models import Post, UserOwner

from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
)
from .forms import AuthenticationForm


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        # print kwargs
        # set form tag attributes
        if 'instance' in kwargs:
            if kwargs['instance']:
                self.helper.form_action = reverse('post_update',
                    kwargs={'pk': kwargs['instance'].id})
            else:
                self.helper.form_action = reverse('post_create')
        else:
            self.helper.form_action = reverse('post_create')
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = False
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        # add buttons
        if 'instance' in kwargs:
            if kwargs['instance']:
                self.helper.layout[-1] = FormActions(
                    Submit('update_button', 'Update', css_class="btn btn-primary"),
                    Submit('cancel_button', 'Cancel', css_class="btn btn-link")
                    )
            else:
                self.helper.layout[-1] = FormActions(
                    Submit('create_button', 'Create', css_class="btn btn-primary"),
                    Submit('cancel_button', 'Cancel', css_class="btn btn-link")
                    )
        else:
            self.helper.layout[-1] = FormActions(
                Submit('create_button', 'Create', css_class="btn btn-primary"),
                Submit('cancel_button', 'Cancel', css_class="btn btn-link")
                )
    no_field = forms.CharField(required=False)


class PostUpdateView(UpdateView):
    model = Post
    template_name = "blogapp/update_create_post.html"
    form_class = PostForm

    def get_success_url(self):
        messages.success(self.request, 'Post #%s successfully updated!' % self.object.id)
        return reverse('user_list')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.info(request, 'Updating post #%s canceled!' % self.get_object().id)
            return HttpResponseRedirect(reverse('user_list'))
        else:
            return super(PostUpdateView, self).post(request, *args, **kwargs)


class PostCreateView(CreateView):
    model = Post
    template_name = "blogapp/update_create_post.html"
    form_class = PostForm
    # initial = {'user': UserOwner.objects.all()[0]}

    def get_success_url(self):
        messages.success(self.request, 'Post #%s successfully created!' % self.object.id)
        return reverse('user_list')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.info(request, 'Creating new post was canceled!')
            return HttpResponseRedirect(reverse('user_list'))
        else:
            return super(PostCreateView, self).post(request, *args, **kwargs)

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        self.initial['user'] = self.request.user
        print self.request.user
        return self.initial.copy()

class UserOwnerListView(ListView):
    model=UserOwner
    template_name="blogapp/users.html"
    context_object_name='users'

    # def get_context_data(self, **kwargs):
    #     context = super(UserOwnerListView, self).get_context_data(**kwargs)
    #     if self.object == self.request.user:
    #         context['posts'] = self.object.blog.posts.all()
    #     else:
    #         context['posts'] = self.object.blog.posts.filter(is_posted=True)
    #
    #     return context


class PostDetailView(DetailView):
    model=Post
    template_name="blogapp/post.html"
    context_object_name='post'

    def get(self, request, **kwargs):
        self.object = self.get_object()
        if self.object.is_posted == False and self.object.user != self.request.user:
            messages.error(self.request, 'You do not allow look unposted data of other users')
            return HttpResponseRedirect(reverse('home'))
        else:
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)


class UserOwnerDetailView(DetailView):
    model=UserOwner
    template_name="blogapp/user_posts.html"
    context_object_name='userowner'

    def get_context_data(self, **kwargs):
        context = super(UserOwnerDetailView, self).get_context_data(**kwargs)
        if self.object == self.request.user:
            context['posts'] = self.object.blog.posts.all()
        else:
            context['posts'] = self.object.blog.posts.filter(is_posted=True)

        return context


@deprecate_current_app
@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request, template_name='registration/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          extra_context=None, redirect_authenticated_user=False):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.POST.get(redirect_field_name, request.GET.get(redirect_field_name, ''))


    if redirect_authenticated_user and request.user.is_authenticated:
        redirect_to = _get_login_redirect_url(request, redirect_to)
        if redirect_to == request.path:
            raise ValueError(
                "Redirection loop for authenticated user detected. Check that "
                "your LOGIN_REDIRECT_URL doesn't point to a login page."
            )
        return HttpResponseRedirect(redirect_to)
    elif request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return HttpResponseRedirect(_get_login_redirect_url(request, redirect_to))
    else:
        form = authentication_form(request)

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)
    # print('redirect_to')
    # print(redirect_to)

    return TemplateResponse(request, template_name, context)

