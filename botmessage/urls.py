from django.urls import path

from . import views


app_name = 'botmessage'
urlpatterns = [
    path('tb/<slug:parse>/', views.tbotMessage, name='tbot_message'),
]