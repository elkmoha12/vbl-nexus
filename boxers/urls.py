from django.urls import path
from . import views

urlpatterns = [
    path('', views.boxers_list, name='boxers'),
    path('clubs/', views.clubs_list, name='clubs'),
]
