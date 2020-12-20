from django.urls import path


from .views import PhotoDetail, PhotoCreate, HealthDataCreate, HealthDataUpdate, DailyLogCreate, DailyLogUpdate, AllRecords, ActivityLogCreate,  PhotoCreate, PhotoList, PhotoDelete
from django.views.generic.dates import DateDetailView
from .models import ActivityLog


app_name = 'health'

urlpatterns = [
#     path('healthdata/<int:user_id>', HealthDataDetail.as_view(),
#          name='healthdata-detail'),
    path('healthdata/create/', HealthDataCreate.as_view(),
         name='healthdata-create'),

    path('healthdata/<int:user_id>/update/', HealthDataUpdate.as_view(),
         name='healthdata-update'),

    #     path('healthdata/<int:id>', HealthDataDetail.as_view(),
    #     name = 'healthdata-detail'),
    path('dailylog/create/', DailyLogCreate.as_view(),
         name='dailylog-create'),
         
    path('dailylog/<str:entry_date>/update/',
         DailyLogUpdate.as_view(), name='dailylog-update'),
    path('records/', AllRecords.as_view(), name='all-records'),
    path('activitylog/create/', ActivityLogCreate.as_view(),
         name='activitylog-create'),
    # path('activity_log/<date>/', ActivityLogList.as_view()),
    path('<int:year>/<str:month>/<int:day>/activitylog/<int:pk>/',
         DateDetailView.as_view(model=ActivityLog, date_field='entry_date', allow_future=False), name='activitylog-date-detail'),
     path('photo/upload/', PhotoCreate.as_view(), name='photo-create'),
     path('photo/<int:pk>/', PhotoDetail.as_view(), name='photo-detail'),
]
