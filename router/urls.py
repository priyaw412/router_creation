from django.urls import path

from . import views

urlpatterns = [
    path('', views.router_list, name='router_list'),
    path('view/<int:pk>', views.router_view, name='router_view'),
    path('new', views.router_create, name='router_new'),
    path('edit/<int:pk>', views.router_update, name='router_list'),
    path('delete/<int:pk>', views.router_delete, name='router_list'),

    ]