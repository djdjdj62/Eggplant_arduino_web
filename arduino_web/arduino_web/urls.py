"""arduino_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from django.conf.urls import include, url
from trips import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url('^hello/$', views.hello_world, name="hellow"),
    url('^vue/$', views.vue, name="vue test"),
    url('^main/$', views.the_page, name="main page"),


    url('^data_put_test/$', views.data_put_test, name="data_put_test"),
    url('^data_get_test_by_get/$', views.data_get_test_by_get, name="data_get_test_by_get"),
    url('^data_get_test_by_post/$', views.data_get_test_by_post, name="data_get_test_by_post"),
    url('^data_get_test_by_html/$', views.data_get_test_by_html, name="data_get_test_by_html"),

    url('^search-post/$', views.search_post),
    #Line_Bot
    url('^line_bot/$', views.line_bot , name="a line_bot on 植物園" ),
    #Api_weather_now
    url('^weather_now_by_web/$', views.weather_now_by_web , name="weather_now" ),
    #Api_weather_future
    url('^weather_future_by_web/$', views.weather_future_by_web , name="weather_now" ),
]
