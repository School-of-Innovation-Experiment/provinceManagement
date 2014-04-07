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
from django.conf import settings
from dajaxice.core import dajaxice_autodiscover, dajaxice_config

dajaxice_autodiscover()

#display django admin page
admin.autodiscover()

#Custome error page
handler500 = 'backend.errorviews.error500'
handler403 = 'backend.errorviews.error403'
handler404 = 'backend.errorviews.error404'


urlpatterns = patterns('',
    # Add this to get widgets.AdminDateWidget() working for non is_staff, is_superuser
    # This must be placed before (r'^admin/(.*)', admin.site.root), as that gobals up everything
    url(r'^admin/jsi18n/$', 'django.views.i18n.javascript_catalog'),

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
        # name="school"
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
        r'^feedback/$',
        direct_to_template, {'template': 'base/feedback.html'},
        name="feedback"
    ),
    url(
        r'^show/',
        include('showtime.urls'),
    ),
    url(
        r'^settings/',
        include("users.urls")
    ),
    url(
        r'^errors/',
        include("backend.urls")
    ),
    url(
        r'^analysis/',
        include("analysis.urls")
    ),
    url(
        r'^rpc/',
        include('rpc.urls'),
        name="rpc",
    ),
)

urlpatterns += patterns('', url(r'tinymce/', include('tinymce.urls')),)
urlpatterns += patterns('', url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),)
urlpatterns += staticfiles_urlpatterns()

# for develop to serve user-upload content in MEDIA_ROOT
if settings.DEBUG:
    urlpatterns += patterns('',
            url(r'media/(?P<path>.*)$',
                'django.views.static.serve',
                {'document_root': settings.MEDIA_ROOT}),
                )
