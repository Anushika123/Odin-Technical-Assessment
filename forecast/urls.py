from django.urls import path
from . import views

urlpatterns = [
     path('', views.index, name='index'),
    path('upload/', views.upload_file, name='upload'),
   path('forecast_view/', views.forecast_view, name='forecast_view')
]