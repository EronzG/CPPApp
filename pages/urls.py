from django.urls import path

from .views import HomePage, Dashboard, DailyInfoView, WeeklyInfoView, MonthlyInfoView

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('dashboard/<int:year>/<str:month>/<int:day>/', DailyInfoView.as_view(), name='daily-archive'),
    # path('today/', TodayInformationView.as_view(), name='archive-today')
    path('dashboard/<int:year>/week-<int:week>/',
         WeeklyInfoView.as_view(), name="weekly-archive"),
    # Example: /2012/aug/
    path('dashboard/<int:year>/month-<str:month>/',
         MonthlyInfoView.as_view(), name="monthly-archive"),
]
