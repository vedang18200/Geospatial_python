from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('map/',views.map,name='map'),
    path('rainfall_analysis/',views.rainfall_analysis,name='rainfall_analysis'),
    path('heatmap/', views.heatmap, name='heatmap'),
    path('bussiness/', views.bussiness, name='bussiness'),
    
]
