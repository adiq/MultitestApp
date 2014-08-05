from django.conf.urls import patterns, url

urlpatterns = patterns('',

                       url(r'^$', 'multitest_admin.views.index', name='index'),
                       url(r'^test/(?P<test_id>\d+)$', 'multitest_admin.views.test', name='test'),
                       url(r'^question/(?P<question_id>\d+)$', 'multitest_admin.views.question', name='question'),


                       )