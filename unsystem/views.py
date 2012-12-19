from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from unsystem.forms import RegistrationForm, ProfileForm
from unsystem.models import UserProfile

import datetime
import hashlib
import random

def create_inactive_user(form):
    username = form.cleaned_data["username"]
    email = form.cleaned_data["email"]
    password = form.cleaned_data["password1"]
    salt = hashlib.sha256(str(random.random())).hexdigest()[:6]
    activation_key = hashlib.sha256(salt + username).hexdigest()
    key_expires = timezone.now() + datetime.timedelta(2)

    user = User.objects.create_user(username, email, password)
    user.is_active = False
    user.save()
    profile = UserProfile(user=user,
                          activation_key=activation_key,
                          key_expires=key_expires)
    profile.save()

    email_subject = "Your new account confirmation"
    email_body = """Hello %s,
Thanks for signing up for an account.

To activate your account, click this link within 48 hours:

    http://127.0.0.1:8000/confirm/%s""" % (username, activation_key)

    send_mail(email_subject, email_body, "foo@bar.org", [email])

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            create_inactive_user(form)
            return render(request, "register.html", {"created": True})
    else:
        form = RegistrationForm()
    return render(request, "register.html", {"form": form})

def confirm(request, activation_key):
    user_profile = get_object_or_404(UserProfile,
                                     activation_key=activation_key)
    if user_profile.key_expires < timezone.now():
        return render(request, "confirm.html", {"expired": True})
    user = user_profile.user
    user.is_active = True
    user.save()
    return render(request, "confirm.html", {"success": True})

def post_login(sender, request, user, **kwargs):
    messages.info(request, "Logged in.")
user_logged_in.connect(post_login)

@login_required
def profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            # leave message
            profile = request.user.get_profile()
            profile.organization = form.instance.organization
            profile.website = form.instance.website
            profile.country = form.instance.country
            profile.bio = form.instance.bio
            profile.contact = form.instance.contact
            profile.save()
    else:
        form = ProfileForm(instance=request.user.get_profile())
    return render(request, "profile.html", {"form": form})

