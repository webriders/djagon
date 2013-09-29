from django.conf.urls import patterns, url
from source.game.views import create_game, play_game, join_random


urlpatterns = patterns('',
    url(r'^create/$', create_game, name='game-create'),
    url(r'^random/$', join_random, name='game-random'),
    url(r'^(?P<game_id>[A-F0-9]{6})/$', play_game, name='game-play'),
)
