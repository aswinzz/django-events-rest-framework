from django.conf.urls import url,include

from . import views

app_name = "events"
urlpatterns = [
    url(r'event$', views.EventApi.as_view(), name='Event'),
]