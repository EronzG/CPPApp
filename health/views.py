import re
from boto3 import client
from datetime import date

from django.conf import settings
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.http import Http404, HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormMixin, CreateView, DeleteView, UpdateView
from django.views.generic.dates import DateDetailView, YearArchiveView, MonthArchiveView, WeekArchiveView, DayArchiveView, TodayArchiveView


from .models import DailyLog, ActivityLog, HealthData, Photo
from .forms import PhotoDownloadForm, DailyLogForm, ActivityLogForm, HealthDataForm, Photoform


def check_user_acccess(data, request):
    '''Confirm if the user can access the data they are requesting'''
    if data.user != request.user:
        raise Http404


# class HealthDataDetail(DetailView):
#     model = HealthData

#     def dispatch(self, request, *args, **kwargs):
#         try:
#             self.get_object()
#             return super().dispatch(request, *args, **kwargs)
#         except self.model.DoesNotExist:
#             return redirect('health:healthdata-create')
#         # if not self.request.user.has_healthdata():
#         #     return redirect('health:healthdata-create')
#         # return super().dispatch(request, *args, **kwargs)

#     def get_object(self):
#         return self.model.objects.get(user__id=self.kwargs['user_id'])

#     def get_context_data(self, **kwargs):
#         data = super().get_context_data(**kwargs)
#         mass = self.get_object().mass
#         height = self.get_object().cm_2_m()
#         bmi = BMI(mass, height)
#         data['bmi'] = bmi
#         data['bmi_report'] = bmi.report()
#         return data


class HealthDataCreate(LoginRequiredMixin, CreateView):
    model = HealthData
    form_class = HealthDataForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class HealthDataUpdate(LoginRequiredMixin, UpdateView):
    model = HealthData
    form_class = HealthDataForm
    context_object_name = 'healthdata'

    def get_object(self, queryset=None):
        return self.model.objects.get(user__id=self.kwargs['user_id'])

    # def get(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     check_user_acccess(self.object, request)
    #     return super().get(request, *args, **kwargs)


class DailyLogCreate(LoginRequiredMixin, CreateView):
    model = DailyLog
    form_class = DailyLogForm

    def dispatch(self, request, *args, **kwargs):
        try:
            today_entry = self.model.objects.get(
                user=self.request.user, entry_date=date.today())
            return redirect('health:dailylog-update', entry_date=str(today_entry.entry_date))
        except self.model.DoesNotExist:
            return super().dispatch(request, *args, **kwargs)
        # if self.model.objects.get(user=self.request.user, entry_date=date.today()).exists():
        #     return redirect('health:dailylog-update')
        # return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DailyLogUpdate(LoginRequiredMixin, UpdateView):
    model = DailyLog
    form_class = DailyLogForm

    def get_object(self, queryset=None):
        return self.model.objects.get(user=self.request.user, entry_date=date.today())

    # success_url = reverse_lazy('health:dailylog-detail')  TODO: make this today view


class ActivityLogCreate(LoginRequiredMixin, CreateView):
    model = ActivityLog
    form_class = ActivityLogForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PhotoCreate(LoginRequiredMixin, CreateView):
    model = Photo
    form_class = Photoform

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PhotoDetail(LoginRequiredMixin, FormMixin, DetailView):
    model = Photo
    form_class = PhotoDownloadForm

    def get_object(self):
        return self.model.objects.get(pk=self.kwargs['pk'])

    def get_success_url(self):
        return reverse_lazy('health:photo-detail', kwargs={'pk': self.get_object().pk})

    def post(self, request, *args, **kwargs):
        s3 = client('s3')
        obj_url = self.get_object().url
        file_name = str(obj_url).split('/')[-1]
        return s3.download_file(settings.AWS_STORAGE_BUCKET_NAME, obj_url, file_name)




class PhotoDelete(LoginRequiredMixin, DeleteView):
    model = Photo
    success_url = reverse_lazy('health:photo-list')


class AllRecords(LoginRequiredMixin, ListView):
    template_name = 'health/records.html'
    model = DailyLog

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        activitylogs = ActivityLog.objects.filter(user=self.request.user)
        data['activitylogs'] = activitylogs
        photos = Photo.objects.filter(user=self.request.user)
        data['photos'] = photos
        return data


# class DailyLogDetail(DetailView):

#     model = DailyLog

#     def get_context_data(self, **kwargs):
#         # Call the base implementation first to get a context
#         context = super().get_context_data(**kwargs)
#         # Add in a QuerySet of all the books
#         context['activity_log_list'] = ActivityLog.objects.all()
#         return context


# class Dashboard(DetailView):
#     model = DailyLog

#     def get_context_data(self, **kwargs):
#         # Call the base implementation first to get a context
#         context = super().get_context_data(**kwargs)
#         # Add in a QuerySet of all the books
#         context['activity_log_list'] = ActivityLog.objects.get()
#         context['daily_log_list'] = DailyLog.objects.all()
#         context['today_log'] = DailyLog.objects.filter(date=date.today)
#         return context


# class ActivityLogList(LoginRequiredMixin, ListView):
#     # default template_name: health/activitylog_list.html
#     # default context_object_name: activity log_list
#     model = ActivityLog
#     paginate_by = 20

#     def get_queryset(self):
#         qs = super().get_queryset()
#         return qs.filter(user=self.request.user)


class PhotoList(LoginRequiredMixin, ListView):
    model = Photo

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)




