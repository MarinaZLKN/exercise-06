from django.urls import path

from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login_view'),
    path('register', views.register_view, name='register_view'),
    path('log_out', views.log_out, name='log_out'),
    path('room_view/<int:pk>', views.room_view, name='room_view'),
    path('room_add', views.room_add, name='room_add'),
    path('room_private_view/<int:user_pk>', views.room_private_view, name='room_private_view'),
]