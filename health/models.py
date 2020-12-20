from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

from .scripts import calculateAge


User = get_user_model()


class HealthData(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'O'

    GENDER_CHOICES = (
        (MALE, _('Male')),
        (FEMALE, _('Female')),
        (OTHER, _('Other')),
    )
    """User's health-related Data"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mass = models.IntegerField(_("weight(kg)"), blank=True, null=True)
    height = models.IntegerField(_("height(cm)"), blank=True, null=True)
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, default=OTHER)
    dob = models.DateField(
        _("date of birth"), auto_now=False, auto_now_add=False, blank=True, null=True)

    #   The following fields are for tracking changes made by a user
    created = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)

    def __str__(self) -> str: self.user

    def get_absolute_url(self):
        #  to be replaced with  if any problems
        return reverse('dashboard')

    def kg_2_pound(self):
        """Converts mass from kg to lb (pound)"""
        # 1kg = 2.20462 lbs
        return self.mass*2.20462

    def cm_2_m(self):
        """Converts height from cm to m"""
        return self.height/100

    def b_m_i(self):
        """Calculates the body mass index"""
        return self.mass/(self.cm_2_m**2)

    def age(self):
        """Calculates user's age from dob"""
        if self.dob:
            return calculateAge(self.dob)
        return "No information on date of birth."


# @receiver(user_signed_up)
# def after_user_signed_up(sender, request, user, **kwargs):
#     HealthData.objects.create(user=user)


class DailyLog(models.Model):
    """Daily input of health related data from user"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    entry_date = models.DateField(auto_now_add=True, null=True)
    steps = models.IntegerField(blank=True, null=True)
    mood = models.CharField(max_length=255)

    class Meta:
        ordering = ["-entry_date"]

    def __str__(self):
        return f"{self.entry_date} ~ {self.mood}"

    def get_absolute_url(self):
        return reverse('dashboard')

    def shortened_mood(self):
        if len(self.mood) > 3:
            return f"{self.mood[:3]}..."
        return self.mood


class Photo(models.Model):
    image = models.ImageField(
        upload_to='images/', height_field=None, width_field=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_uploaded = models.DateField(auto_now_add=True, null=True)
    caption = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.caption} ~ {self.date_uploaded}"

    def get_absolute_url(self):
        return reverse('dashboard')


class ActivityLog(models.Model):
    JOGGING = 1
    SWIMMING = 2
    CYCLING = 3
    YOGA = 4
    MOUNTAINEERING = 5
    BASKETBALL = 6
    SOCCER = 7
    NAPPING = 8
    READING = 9
    OTHER = 10

    ACTIVITY_CHOICES = (
        (JOGGING, _('Jogging')),
        (SWIMMING, _('Swimming')),
        (CYCLING, _('Cycling')),
        (YOGA, _('Yoga')),
        (MOUNTAINEERING, _('Mountaineering')),
        (BASKETBALL, _('Basketball')),
        (SOCCER, _('Soccer')),
        (NAPPING, _('Napping')),
        (READING, _('Reading')),
        (OTHER, _('Other')),
    )
    """Log Activity sessions like game, yoga etc."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    entry_date = models.DateField(auto_now_add=True)
    activity = models.PositiveSmallIntegerField(choices=ACTIVITY_CHOICES)
    duration = models.IntegerField(_('Duration (minuites)'), blank=True, null=True)

    class Meta:
        ordering = ["-entry_date"]

    def __str__(self):
        return self.get_activity_display()

    def get_absolute_url(self):
        return reverse('dashboard')
