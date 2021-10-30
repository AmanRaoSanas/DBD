from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('proc', views.proc, name='proc'),
    path('team', views.team, name='team'),
]