from django.conf.urls import patterns, include, url
import socketio.sdjango


socketio.sdjango.autodiscover()


djagon_urlpatterns = patterns(
    '',
    url(r'^', include('home.urls')),
    url(r'^game/', include('game.urls')),
)

urlpatterns = patterns(
    '',
    url('^socket\.io', include(socketio.sdjango.urls)),
    url('^', include(djagon_urlpatterns, namespace='djagon')),
)
