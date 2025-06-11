# hospital/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.upload_file, name='upload_file'),
    path('results/', views.show_results, name='show_results'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)