from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('map/',views.map,name='map'),
    path('rainfall_analysis/',views.rainfall_analysis,name='rainfall_analysis'),
    path('heatmap/', views.heatmap, name='heatmap'),
    path('bussiness/', views.bussiness, name='bussiness'),
    path('hmap/', views.hmap, name='hmap'),
    path('compare/', views.compare_states, name='compare_states'),
    path('realestate_map/', views.realestate_map,name='realestate_map'),
    path('compare_realestate/', views.compare_realestate,name='compare_realestate'),
    path('agriculture_map/',views.agriculture_map,name='agriculture_map'),
    path('state_analysis/<str:state_name>/',views.state_analysis,name='state_analysis'),
    
    
]
