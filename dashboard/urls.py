from django.conf.urls import patterns, include, url
from django.contrib import admin
from dashboard.views import IndexView, DeployView, InventoryView, ApplicationView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'deliverman.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'/deploy/$', DeployView.as_view(), name='dashboard.deploy'),
    url(r'/inventory/$', InventoryView.as_view(), name='dashboard.inventory'),
    url(r'/project/$', ApplicationView.as_view(), name='dashboard.application'),
    url(r'/$', IndexView.as_view(), name='dashboard.index'),
)
