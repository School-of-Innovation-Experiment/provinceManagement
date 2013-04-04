"""
    Author: tianwei
    Email: liutianweidlut@gmail.com
    Description: main settings of Chemistry Tools Site
    Created: 2013-3-10
"""

from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from users import views as users_views
from dajaxice.core import dajaxice_autodiscover, dajaxice_config

dajaxice_autodiscover()

#display django admin page
admin.autodiscover()

#Custome error page
handler500 = 'backend.errorviews.error500'
handler403 = 'backend.errorviews.error403'
handler404 = 'backend.errorviews.error404'


urlpatterns = patterns('',
    url(
        r'^',
        include('news.urls'),
        name="news"
    ),
    url(
        r'^admin/',
        include(admin.site.urls),
    ),
    url(
        r'^accounts/',
        include('registration.urls'),
    ),
    url(
        r'^school/',
        include('school.urls'),
        name="school"
    ),
    url(
        r'^expert/',
        include('expert.urls'),
    ),
    url(
        r'^adminStaff/',
        include('adminStaff.urls'),
        name="adminstaff_home"
    ),
    url(
        r'^features/$',
        direct_to_template, {'template': 'introduction/features.html'},
        name="features"
    ),
    url(
        r'^show/$',
        include('showtime.urls'),
    ),
)

# urlpatterns += staticfiles_urlpatterns()
urlpatterns += patterns('', url(r'tinymce/', include('tinymce.urls')),)
urlpatterns += patterns('', url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),)
urlpatterns += staticfiles_urlpatterns()
