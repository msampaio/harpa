from django.conf.urls import patterns, include, url
from django.contrib import admin
from dispositions import views
from django.utils.translation import ugettext_lazy as _


handler404 = views.error404
handler500 = views.error500


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'harp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.home, name='home'),
    url(_(r'^all/'), views.show_all_settings, name='show_all_settings'),
    url(r'^download/', views.download_all_settings, name='download_all_settings'),
    url(_(r'^index$'), views.get_by_index, name='get_by_index'),
    url(_(r'^prime$'), views.get_by_prime, name='get_by_prime'),
    url(_(r'^accidents$'), views.get_by_accidents, name='get_by_accidents'),
    url(_(r'^index/(?P<pedal_index>\d+)/$'), views.show_settings_by_index, name='show_settings_by_number'),
    url(_(r'^prime/(?P<pedal_prime>\w+)/$'), views.show_settings_by_prime, name='show_settings_by_prime'),
    url(_(r'^accidents/(?P<accidents>\w+)/$'), views.show_settings_by_accidents, name='show_settings_by_accidents'),
    url(_(r'^statistics/$'), views.show_statistics, name='show_statistics'),
    url(r'^admin/', include(admin.site.urls)),
)
