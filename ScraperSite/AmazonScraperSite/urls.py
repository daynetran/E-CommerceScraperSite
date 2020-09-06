
from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing_page),
    path('help/', views.help),
    path('download_page/', views.download_page),
]

urlpatterns += staticfiles_urlpatterns()
