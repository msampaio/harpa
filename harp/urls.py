from django.conf.urls import patterns, include, url
from django.contrib import admin
from dispositions import views
from django.utils.translation import ugettext_lazy as _


handler404 = views.error404
handler500 = views.error500


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'harp.views.dashboard', name='dashboard'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.home, name='home'),
    url(_(r'^about/$'), views.about, name='about'),
    url(_(r'^dashboard/$'), views.dashboard, name='dashboard'),
    url(_(r'^dashboard/all/$'), views.show_all_settings, name='show_all_settings'),
    url(r'^dashboard/download/$', views.download_all_settings, name='download_all_settings'),
    url(_(r'^dashboard/index$'), views.get_by_index, name='get_by_index'),
    url(_(r'^dashboard/prime$'), views.get_by_prime, name='get_by_prime'),
    url(_(r'^dashboard/accidents$'), views.get_by_accidents, name='get_by_accidents'),
    url(_(r'^dashboard/index/(?P<pedal_index>\d+)/$'), views.show_settings_by_index, name='show_settings_by_number'),
    url(_(r'^dashboard/prime/(?P<pedal_prime>\w+)/$'), views.show_settings_by_prime, name='show_settings_by_prime'),
    url(_(r'^dashboard/accidents/(?P<accidents>\w+)/$'), views.show_settings_by_accidents, name='show_settings_by_accidents'),
    url(_(r'^dashboard/statistics/$'), views.show_statistics, name='show_statistics'),
    url(r'^admin/$', include(admin.site.urls)),
)
