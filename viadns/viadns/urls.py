from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'viadns.views.home', name='home'),
    # url(r'^viadns/', include('viadns.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    
    url(r'^$', 'viadns.views.index'),
    url(r'^signup', 'account.views.signup'),
    url(r'^login', 'account.views.login'),
    url(r'^logout', 'account.views.logout'),
    url(r'^dashboard', 'account.views.dashboard'),
)
