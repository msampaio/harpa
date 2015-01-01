from django.conf.urls import patterns, include, url
from django.contrib import admin
from dispositions import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'harp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.home, name='home'),
    url(r'^all/', views.show_all_settings, name='show_all_settings'),
    url(r'^download/', views.download_all_settings, name='download_all_settings'),
    url(r'^index$', views.get_by_index, name='get_by_index'),
    url(r'^prime$', views.get_by_prime, name='get_by_prime'),
    url(r'^accidents$', views.get_by_accidents, name='get_by_accidents'),
    url(r'^index/(?P<pedal_number>\d+)/$', views.show_combination_by_index, name='show_settings_by_number'),
    url(r'^prime/(?P<pedal_prime>\w+)/$', views.show_combination_by_prime, name='show_settings_by_prime'),
    url(r'^accidents/(?P<accidents>\w+)/$', views.show_combination_by_accidents, name='show_settings_by_accidents'),
    url(r'^admin/', include(admin.site.urls)),
)
