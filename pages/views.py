import math
import decimal
from datetime import date, timedelta

from django.db.models.aggregates import Sum, Count
from django.http import request
from BMI_calc_pkg.bmi_calc import BMI
from django.db.models import BigIntegerField
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.views.generic.dates import DayArchiveView, TodayArchiveView, DateDetailView, WeekArchiveView, MonthArchiveView

from health.models import DailyLog, ActivityLog, HealthData, Photo
from health.recommender import DailyStepsRecommendation, DailyActivityRecommendation


def get_object_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None


def get_last_n_objects(classmodel, n, **kwargs):
    if classmodel.objects.count() < n:
        return classmodel.objects.filter(**kwargs)
    return classmodel.objects.filter(**kwargs).order_by('-entry_date')[:n][::-1]


class HomePage(TemplateView):
    template_name = 'home.html'



class DailyInfoView(DayArchiveView):
    template_name = 'daily_archive.html'
    model = ActivityLog
    date_field = 'entry_date'
    allow_empty = True

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        healthdata = get_object_or_none(HealthData, user=self.request.user)
        data['healthdata'] = healthdata

        if healthdata:
            mass = healthdata.mass
            height = healthdata.cm_2_m()
            bmi = BMI(mass, height)
            data['bmi'] = bmi

        dailylog = get_object_or_none(DailyLog, user=self.request.user,
                                      entry_date__day=self.get_day())

        data['photos'] = get_last_n_objects(Photo, 20, user=self.request.user,
                                            date_uploaded=self.day)

        if dailylog:
            steps_report = DailyStepsRecommendation(
                dailylog.steps, 1).evaluate()
            data['steps_report'] = steps_report
        return data


class Dashboard(LoginRequiredMixin, TodayArchiveView, DailyInfoView):
    template_name = 'dashboard.html'
    def get_queryset(self):
        qs = super(DailyInfoView, self).get_queryset()
        return qs.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        data = super(DailyInfoView, self).get_context_data(**kwargs)
        
        healthdata = get_object_or_none(HealthData, user=self.request.user)
        data['healthdata'] = healthdata

        if healthdata:
            mass = healthdata.mass
            height = healthdata.cm_2_m()
            bmi = BMI(mass, height)
            data['bmi'] = bmi

        dailylog = get_object_or_none(DailyLog, user=self.request.user,
                                      entry_date=date.today())
        data['dailylog'] = dailylog

        data['photos'] = get_last_n_objects(Photo, 20, user=self.request.user,
                                            date_uploaded=date.today())

        if dailylog:
            steps_report = DailyStepsRecommendation(
                dailylog.steps, 1).evaluate()
            data['steps_report'] = steps_report
        
        if data['object_list']:
            activities = data['object_list']
            activity_count = activities.count()
            data['activity_count'] = activity_count
            # minutes = sum([(m.duration.seconds//60) for m in self.get_dated_queryset()])
            activity_period = sum([m.duration for m in activities])
            print(activity_period)
            activity_report = DailyActivityRecommendation(activity_period, 1).evaluate()
            data['activity_report'] = activity_report

        return data


class WeeklyInfoView(LoginRequiredMixin, WeekArchiveView):
    template_name = 'weekly_archive.html'
    model = ActivityLog
    date_field = 'entry_date'
    allow_empty = True
    allow_future = False

    def get_queryset(self):
        qs = super(WeekArchiveView, self).get_queryset()
        return qs.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        data = super(WeekArchiveView, self).get_context_data(**kwargs)

        dailylogs = get_last_n_objects(DailyLog, 8, user=self.request.user,
                                      entry_date__gte=data['week'])
        data['dailylogs'] = dailylogs

        if dailylogs:
            weekly_steps = dailylogs.aggregate(Sum('steps', output_field=BigIntegerField()))
            log_count = dailylogs.count()
            steps_report = DailyStepsRecommendation(
                weekly_steps['steps__sum'], log_count).evaluate()
            data['steps_report'] = steps_report

        return data



class MonthlyInfoView(LoginRequiredMixin, MonthArchiveView):
    model = ActivityLog
    paginate_by = 20
    date_field = "entry_date"
    allow_future = False
    allow_empty = True

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        

        return data
