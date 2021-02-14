from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('', views.router_list, name='router_list'),
    path('view/<int:pk>', views.router_view, name='router_view'),
    path('new', views.router_create, name='router_new'),
    path('edit/<int:pk>', views.router_update, name='router_edit'),
    path('delete/<int:pk>', views.router_delete, name='router_delete'),
    url(r'^create-router/$', views.CreateRouterDevice.as_view(), name='create_router'),
    url(r'^$', views.RouterListAPIView.as_view(), name='show_list'),
    url(r'^(?P<ip_addr>[^/]+)/router/$', views.RouterBasedonIPRUDView.as_view(),
        name='update-delete-router'),

]