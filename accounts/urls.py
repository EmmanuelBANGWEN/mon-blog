from django.urls import path
from . import views

urlpatterns = [

    path('login/', views.login_views, name='login_views'),
    path('logout/', views.logout_views, name='logout_views'),
    path('register/', views.register_views, name='register_views'),

]