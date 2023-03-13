from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from users.models import Profile
from users.forms import ProfileModelForm


def register(request):
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('topics:index')
    return render(request, 'registration/register.html', {'form': form})


def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    confirm = False
    form = ProfileModelForm(request.POST or None, request.FILES or None, instance=profile)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
        confirm = True
    return render(request, 'users/profile.html', {'user': user, 'profile': profile, 'form': form, 'confirm': confirm})


def profiles_list(request):
    user = request.user
    queryset = Profile.objects.get_all_profiles(user)
    return render(request, 'users/profiles_list.html', {'queryset': queryset})


class ProfileDetailView(DetailView, LoginRequiredMixin):

    model = Profile
    template_name = 'users/detail.html'

    def get_object(self, slug=None):
        slug = self.kwargs.get('slug')
        profile = Profile.objects.get(slug=slug)
        return profile

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.views += 1
        self.object.save()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)



# def profile_detail(request, slug):
#     profile = Profile.objects.get(slug=slug)
#     return render(request, 'users/detail.html', {'profile': profile})
