from django.conf.urls import patterns, include, url


djagon_urlpatterns = patterns(
    '',
    url(r'^', include('home.urls')),
)

urlpatterns = patterns(
    '',
    url('^', include(djagon_urlpatterns, namespace='djagon')),
)
