from django import forms
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True, editable=False)
    activation_key = models.CharField(max_length=64, editable=False)
    key_expires = models.DateTimeField(editable=False)

    # First name, last name and email already part of django auth
    organization = models.CharField(max_length=50, blank=True)
    website = models.URLField(blank=True)
    country = models.CharField(max_length=50, blank=True)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to="photos", null=True, blank=True)
    contact = models.TextField(blank=True)

class Talk(models.Model):
    # A user can register multiple talks
    user_profile = models.ForeignKey(UserProfile, editable=False)
    title = models.CharField(max_length=100, blank=True)
    abstract = models.TextField(blank=True)

class Ticket(models.Model):
    user_profile = models.ForeignKey(UserProfile, editable=False)
    bitcoin_addr = models.CharField(max_length=50)
    paypal_email = models.EmailField(blank=True)
    sepa_code = models.CharField(max_length=8, editable=False)
    ticket_code = models.CharField(max_length=6, editable=False)
    active = models.BooleanField(default=False)

