from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    path("new/", views.new_entry, name="new_entry"),
    path("checkin/", views.daily_checkin, name="daily_checkin"),
    path("analysis/", views.analysis, name="analysis"),
    path("about/", views.about, name="about"),
]
