from django.conf.urls import patterns, include, url


djagon_urlpatterns = patterns(
    '',
    url(r'^', include('home.urls')),
    url(r'^game/', include('game.urls')),
)

urlpatterns = patterns(
    '',
    url('^', include(djagon_urlpatterns, namespace='djagon')),
)
