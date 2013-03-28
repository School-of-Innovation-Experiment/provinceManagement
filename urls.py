"""
    Author: tianwei
    Email: liutianweidlut@gmail.com
    Description: main settings of Chemistry Tools Site
    Created: 2013-3-10
"""

from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.contrib import admin

#from gui import views as gui_views
from users import views as users_views


admin.autodiscover()

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
                       url(
        r'^',
        include('news.urls'),
        name="news"
    ),
    # url(
    #     r'^$',
    #     direct_to_template, {'template': 'home/index.html'},
    #     name='index'
    # ),
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
    ),
    url(
        r'^features/$',
        direct_to_template, {'template': 'introduction/features.html'},
        name="features"
    ),
    url(
        r'^show/$',
        direct_to_template, {'template': 'introduction/show.html'},
    ),
)

urlpatterns += patterns('', url(r'tinymce/', include('tinymce.urls')),)
