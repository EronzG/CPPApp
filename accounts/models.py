
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _


class CustomUser(AbstractUser):
    """User information for authentication purpose"""
    name = models.CharField(_('full name'), max_length=30,
                            blank=False, null=False, default='User')

    def __str__(self):
        return self.get_first_name()  # self.get_short_name()

    def get_full_name(self):
        return self.name.strip()

    def get_first_name(self):
        """Return first name for the user."""
        first_name = self.name.split()[0]
        return first_name.strip()

    def has_healthdata(self):
        return hasattr(self, 'healthdata')
