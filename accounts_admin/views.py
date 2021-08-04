from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib import messages

from .forms import UserRegisterForm, UserLoginForm, ProfileForm


class HomeView(LoginView):
    template_name = 'registration/login.html'


class LogOut(LoginRequiredMixin, LogoutView):
    template_name = 'registration/logged_out.html'


def login_user(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            pw = form.cleaned_data['password']
            user = authenticate(username, pw)

            if user is None:
                print('user is none.')

            login(request, user)
            return HttpResponseRedirect(reverse('accounts_admin:home'))
    else:
        form = UserLoginForm()
    return render(request, 'registration/login.html', {'form': form})


def index(request):
    return render(request, 'accounts_admin/index.html')


def root(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('accounts_admin:home'))
    else:
        return HttpResponseRedirect(reverse('accounts_admin:login'))


class UserCreateView(CreateView):
    template_name = 'registration/sign_up.html'
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('accounts_admin:home')

    def form_valid(self, form):
        response = super(UserCreateView, self).form_valid(form)
        username = form.cleaned_data.get('username')
        pw = form.cleaned_data.get('password1')
        new_user = authenticate(self.request, username=username, password=pw)
        if new_user is not None:
            login(self.request, new_user)
        return response


'''
class UserCreateView(CreateView):
    template_name = 'registration/sign_up.html'
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('receipts:receipts-list')

    def get_context_data(self, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context['profile_form'] = ProfileForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        profile_form = ProfileForm(request.POST, request.FILES)
        if form.is_valid and profile_form.is_valid():
            return self.form_valid(form, profile_form)
        else:
            return self.form_invalid(form, profile_form)

    def form_valid(self, form, profile_form):
        form.save()
        username = form.cleaned_data.get('username')
        pw = form.cleaned_data.get('password1')
        new_user = authenticate(self.request, username=username, password=pw)
        if new_user is not None:
            login(self.request, new_user)
        profile_form.instance = new_user
        profile_form.save()
        messages.success(self.request, 'A new user is created.')
        return HttpResponseRedirect(reverse('accounts_admin:home'))

    def form_invalid(self, form, profile_form):
        return self.render_to_response(self.get_context_data(form=form, profile_form=profile_form))
'''


class ProfileUpdateView(UpdateView):
    template_name = 'accounts_admin/update_profile.html'
    model = User
    fields = ('username', 'email', )
    success_url = reverse_lazy('accounts_admin:home')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super(ProfileUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['profile_form'] = ProfileForm(self.request.POST, self.request.FILES, instance=self.object.profile)
        else:
            context['profile_form'] = ProfileForm(instance=self.object.profile)
        return context

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        profile_form = ProfileForm(self.request.POST, self.request.FILES, instance=self.object.profile)
        if form.is_valid() and profile_form.is_valid():
            return self.form_valid(form, profile_form)
        else:
            return self.form_invalid(form, profile_form)

    def form_valid(self, form, profile_form):
        form.save()
        profile_form.save()
        messages.success(self.request, 'Your profile is updated.')
        return HttpResponseRedirect(reverse('accounts_admin:home'))

    def form_invalid(self, form, profile_form):
        return self.render_to_response(self.get_context_data(form=form, profile_form=profile_form))

