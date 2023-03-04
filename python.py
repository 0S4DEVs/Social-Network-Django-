from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile, Update, FriendRequest

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            Profile.objects.create(user=user)
            return redirect('profiles:view', username=user.username)
    else:
        form = UserCreationForm()
    return render(request, 'profiles/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profiles:view', username=user.username)
    else:
        form = AuthenticationForm()
    return render(request, 'profiles/login.html', {'form': form})

@login_required
def view_profile(request, username):
    user = User.objects.get(username=username)
    profile = user.profile
    updates = Update.objects.filter(user=user).order_by('-timestamp')
    if request.method == 'POST':
        friend_request = FriendRequest.objects.create(from_user=request.user, to_user=user)
        return redirect('profiles:view', username=username)
    else:
        return render(request, 'profiles/view_profile.html', {'profile': profile, 'updates': updates})

@login_required
def add_friend(request, username):
    user = User.objects.get(username=username)
    request.user.profile.friends.add(user.profile)
    request.user.profile.save()
    return redirect('profiles:view', username=username)

@login_required
def create_update(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        update = Update.objects.create(user=request.user, content=content)
        return redirect('profiles:view', username=request.user.username)
    else:
        return render(request, 'profiles/create_update.html')
