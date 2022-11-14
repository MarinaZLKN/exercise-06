from django.urls import path

from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login_view'),
    path('register', views.register_view, name='register_view'),
    path('log_out', views.log_out, name='log_out'),
    path('room_view', views.room_view,name='room_view'),
    path('room_add', views.room_add, name='room_add'),
]