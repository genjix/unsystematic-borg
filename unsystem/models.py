from django import forms
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    activation_key = models.CharField(max_length=64)
    key_expires = models.DateTimeField()

    # First name, last name and email already part of django auth
    organisation = models.CharField(max_length=50)
    website = models.URLField()
    country = models.CharField(max_length=50)
    bio = models.TextField()
    photo = models.ImageField(upload_to="photos")
    contact = models.CharField(max_length=100)

class Talk(models.Model):
    # A user can register multiple talks
    user_profile = models.ForeignKey(UserProfile)
    title = models.CharField(max_length=100)
    abstract = models.TextField()

class Ticket(models.Model):
    user_profile = models.ForeignKey(UserProfile)
    bitcoin_addr = models.CharField(max_length=50)
    paypal_email = models.CharField(max_length=100, null=True)
    sepa_code = models.CharField(max_length=8)
    ticket_code = models.CharField(max_length=6)
    paid = models.BooleanField(default=False)

