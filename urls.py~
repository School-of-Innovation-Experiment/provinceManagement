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
        r'^$',
        direct_to_template, {'template': 'home/index.html'},
        name='index'
    ),
    url(
        r'^admin/',
        include(admin.site.urls),
        name="admin"
    ),
    url(
        r'^accounts/',
        include('registration.urls'),
        name="accounts"
    ),
      url(
        r'^school/',
        include('school.urls'),
        name="school"
    ),
    url(
        r'^project/',
        include('project.urls'),
        name="project"
    ),
    url(
        r'^expert/',
        include('expert.urls'),
        name="expert"
    ),
    url(
        r'^adminStaff/',
        include('adminStaff.urls'),
        name="staff"
        ),
    url(
        r'^facultyStaff/',
        include('facultyStaff.urls'),
        name="staff"
        ),
    url(
        r'^news/',
        include('news.urls'),
        name="news"
    ),
    url(
        r'^showtime/$',
       	include('showtime.urls'),
       	name = "showtime"
    ),
    url(
        r'^newtask/$',
        direct_to_template, {'template': 'features/newtask.html'},
        #gui_views.basic_search
    ),
    url(
        r'^history/$',
        direct_to_template, {'template': 'features/history.html'},
        name="history"
    ),
    url(
        r'^details/$',
        direct_to_template, {'template': 'features/details.html'},
        name="details"
    ),
    url(
        r'^statistics/$',
        direct_to_template, {'template': 'features/statistics.html'},
        name="statistics"
    ),
    url(
        r'^features/$',
        direct_to_template, {'template': 'introduction/features.html'},
        name="features"
    ),
    url(
        r'^show/$',
        direct_to_template, {'template': 'introduction/show.html'},
        name="show"
    ),
    url(
        r'^settings/profile/$',
        #direct_to_template, {'template': 'widgets/settings/profile.html'},
        users_views.profile
    ),
    url(
        r'^settings/admin/$',
        #direct_to_template, {'template': 'widgets/settings/admin.html'},
        users_views.admin_account
    ),

)

urlpatterns += patterns('',
    url(r'tinymce/', include('tinymce.urls')),
)
