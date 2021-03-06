"""travel_assist_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from travel_assist_app import views as app_views
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'index/$', app_views.index, name='index'),
    url(r'^$', schema_view, name='index'),
    url(r'^home/', app_views.home, name='home'),

    url(r'^countries/', app_views.ViewCountries.as_view(), name='countries'),

    url(r'^cities/(?P<country>[\w\s]+)/', app_views.ViewCities.as_view(), name='view_cities'),
    url(r'^cities/$', app_views.CreateCity.as_view(), name='create_citie'),

    url(r'^places/(?P<country>[\w\s]+)/(?P<city>[\w\s]+)/', app_views.ViewPlaces.as_view(), name='places'),
    url(r'^place/(?P<id>[\d]+)/', app_views.ViewPlace.as_view(), name='single_place'),
    url(r'^place/$', app_views.CreatePlace.as_view(), name='create_place'),

    url(r'places_lists/$', app_views.CreatePlacesList.as_view(), name='create_places_list'),
    url(r'my_lists/$', app_views.ViewUserLists.as_view(), name='user_lists'),
    url(r'my_lists/(?P<list_id>[0-9]+)/$', app_views.ViewUserList.as_view(), name='user_list_by_id'),

    url(r'^signup/', app_views.SignupUser.as_view(), name='signup'),
    url(r'^auth/', include('rest_framework.urls')),
    # url(r'/user_lists/(?P<list_id>[0-9]+)/$', app_views.ViewUserLists.as_view(), name='user_lists_del'),
    # url(r'^(?P<pk>[0-9]+)/user/', app_views.ViewUser.as_view(), name='view_user'),
]

