from django.urls import path
from . import views

app_name = 'mosiauth'

urlpatterns = [
    path('loginsss/', views.login_view, name='loginsss'),
    path('logout/',views.logout_view,name='logout'),
    path('img_captcha/',views.img_captcha,name='img_captcha'),
    path('sms_captcha/',views.sms_captcha,name='sms_captcha'),
    path('register/',views.register,name='register'),

]