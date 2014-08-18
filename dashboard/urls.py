from django.conf.urls import patterns, include, url
from django.contrib import admin
from dashboard.views import IndexView, DeployView, InventoryView, ProjectView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'deliverman.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'/$', IndexView.as_view(), name='dashboard.index'),
    url(r'/deploy/$', DeployView.as_view(), name='dashboard.deploy'),
    url(r'/inventory/$', InventoryView.as_view(), name='dashboard.inventory'),
    url(r'/project/$', ProjectView.as_view(), name='dashboard.project'),
)
