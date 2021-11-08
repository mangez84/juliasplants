from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField


class UserProfile(models.Model):
    """A model to store user profiles with contact details."""
    class Meta:
        verbose_name_plural = 'User Profiles'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100, null=False, blank=False)
    city = models.CharField(max_length=50, null=False, blank=False)
    postcode = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(
        blank_label='Select Country', null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)

    def __str__(self):
        return self.user.username
