from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

# Create your views here.

def users(requests):
    return render(requests,"users/users.html")

def profile(request, username):
    context = {
        "username":username,
    }
    return render(request, "users/profile.html",context)


@require_POST
def follow(request, user_id):
    if request.user.is_authenticated:
        member = get_object_or_404(get_user_model(), pk=user_id)
        if member != request.users:
            if member.followers.filter(pk=request.user.pk).exists():
                member.followers.remove(request.user)
            else:
                member.followers.add(request.user)
        return redirect("users:profile", member.username)
    return redirect("accounts:login")