from django.urls import path # type: ignore
from . import views

urlpatterns = [
    path('', views.upload_and_forecast, name='upload_forecast'),
]