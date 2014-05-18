from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^knowledge/', include('knowledge.urls',namespace='knowledge')),
	url(r'^admin/', include(admin.site.urls)),
	# Examples:
    # url(r'^$', 'gamedb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^knowledge/search/$', include('knowledge.urls',namespace='knowledge')),
)
