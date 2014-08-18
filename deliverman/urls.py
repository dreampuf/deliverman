from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'deliverman.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin', include(admin.site.urls)),
    url(r'^accounts', include('accounts.urls')),
    url(r'^dashboard', include('dashboard.urls')),
)


# ... the rest of your URLconf here ...

urlpatterns += staticfiles_urlpatterns()
