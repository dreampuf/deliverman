from django.conf.urls import patterns, include, url
from django.contrib import admin
#from django.contrib.auth.views import login
#from accounts.views import IndexView
from accounts.forms import AccountsAuthentcationForm

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'deliverman.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'/login/$', 'django.contrib.auth.views.login',
            {
                'template_name': 'login.html',
                'authentication_form': AccountsAuthentcationForm
            }, name='accounts.login'),
    url(r'/logout/$', 'django.contrib.auth.views.logout', {
        'next_page': '../login/',
        }, name='accounts.logout'),
)
