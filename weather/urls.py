from django.conf.urls import url
from . import views

app_name = 'weather'
#including all html pages
#in url patterns the url() function matches the regular expression(r) after ^ and then takes it to the function in views.py whose name is specified in name
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<pid1>[0-9]+)/$', views.pindex, name='detail'),
    url(r'^graph/', views.graph, name='graph'),
    url(r'^login/', views.login_user,name='login_user'),
    url(r'^register/', views.register,name='register'),
    url(r'^maps/', views.maps, name='maps'),
    url(r'^logout/', views.logout_user, name='logout'),
    url(r'^plants/', views.plants, name='plants'),
    url(r'^addplants/', views.addplants, name='addplants'),
    url(r'^removeplants/', views.removeplants, name='removeplants'),

]