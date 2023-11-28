
from django.contrib import admin
from django.urls import path
from myCRM import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home,name='home'),
    path('logout/', views.user_logout,name='logout'),
    path('Register/', views.Register_user,name='register'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',  views.activate, name='activate'),
    path('record/<int:pk>', views.customer_record,name='record'),
    path('delete_record/<int:pk>', views.delete_record,name='delete'),  
    path('add_record/', views.add_record,name='add_record'),
    path('update_record/<int:pk>', views.update_record,name='update'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('ChangePassword/', views.Change_Password,name='ChangePassword'),
    
]
