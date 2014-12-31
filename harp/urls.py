from django.conf.urls import patterns, include, url
from django.contrib import admin
from dispositions import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'harp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.home, name='home'),
    url(r'^all/', views.show_all_dispositions, name='show_all_dispositions'),
    url(r'^number$', views.get_number, name='get_number'),
    url(r'^prime$', views.get_prime, name='get_prime'),
    url(r'^accidents$', views.get_accidents, name='get_accidents'),
    url(r'^number/(?P<pedal_number>\d+)/$', views.show_combination_by_number, name='show_combination_by_number'),
    url(r'^prime/(?P<pedal_prime>\w+)/$', views.show_combination_by_prime, name='show_combination_by_prime'),
    url(r'^accidents/(?P<accidents>\w+)/$', views.show_combination_by_accidents, name='show_combination_by_accidents'),
    url(r'^admin/', include(admin.site.urls)),
)
