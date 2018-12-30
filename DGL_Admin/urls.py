"""DGL_Admin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from . import views

handler404 = 'DGL_Admin.views.handler404'
handler500 = 'DGL_Admin.views.handler500'

urlpatterns = [
    path('', views.home, name='home'),
    path('sign_out', views.sign_out, name='sign_out'),

    path('user', views.user, name='user'),
    path('user/add_user', views.add_user, name='add_user'),
    path('user/delete_user/<int:id>', views.delete_user, name='delete_user'),
    path('user/edit_user/<int:id>', views.edit_user, name='edit_user'),

    path('festival', views.festival, name='festival'),
    path('festival/add_festival', views.add_festival, name='add_festival'),
    path('festival/delete_festival/<int:id>', views.delete_festival, name='delete_festival'),
    path('festival/edit_festival/<int:id>', views.edit_festival, name='edit_festival'),

    path('festival/<int:id>/poi/', views.poi, name='poi'),
    path('festival/<int:id_fest>/delete_poi/<int:id_poi>', views.delete_poi, name="delete_poi"),

    path('festival/<int:id_fest>/pois/<int:id_poi>/artists', views.add_artist, name='add_artist'),
    path('festival/<int:id_fest>/pois/<int:id_poi>/delete_artist/<int:id_artist>', views.delete_artist,
         name='delete_artist'),
]
