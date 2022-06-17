from django.urls import include,path

from . import views

urlpatterns =[
    path('',views.index),
    path('login',views.login, name='login'),
    path('map',views.map, name='map'),
]
