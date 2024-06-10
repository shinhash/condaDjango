from django.urls import path
from . import views

urlpatterns = [
    path('post/list/', views.post_list, name='post/list'),
    path('post/create/', views.post_create, name='post/create'),
    path('post/detail/', views.post_detail, name='post/detail'),
    path('post/update/', views.post_update, name='post/update'),
    path('post/delete/', views.post_delete, name='post/delete'),
]