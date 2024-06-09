from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.signin, name='sign/signin'),
    path('signup/', views.signup, name='sign/signup'),
    path('signup/', views.signup, name='sign/signout'),
]
