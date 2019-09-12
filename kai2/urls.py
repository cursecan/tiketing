from django.urls import path

from . import views

app_name = 'kai2'
urlpatterns = [
    path('', views.HomeTemplateView.as_view(), name='index'),
    path('api/cities/', views.cityListJson, name='city_json'),
    path('api/post-schedule/', views.scheduleListJson, name='post_schedule'),
    path('api/bk/<int:id>/passenger/', views.passengerPostView, name='passenger'),
    path('api/bk/<int:id>/wl/', views.waitingListActionView, name='wl_confirm'),
    path('checkin/', views.checkinPostView, name='checkin'),
    path('checkin/<int:pk>/', views.TemplateDetailCheckin.as_view(), name='detail_checkin'),
    path('bookinglist/', views.BookedHistoryListView.as_view(), name='booked_history'),
    path('booking/<int:pk>/', views.TemplateBookingView.as_view(), name='booking'),
]