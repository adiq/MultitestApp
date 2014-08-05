from django.conf.urls import patterns, url

urlpatterns = patterns('',

                       url(r'^$', 'multitest.views.index', name='index'),
                       url(r'^test/(?P<test_id>\d+)$', 'multitest.views.test', name='test'),
                       url(r'^zaloguj$', 'multitest.views.login', name='login'),
                       url(r'^wyloguj$', 'multitest.views.logout', name='logout'),
                       url(r'^rejestracja$', 'multitest.views.register', name='register'),


                       )