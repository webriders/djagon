import jsonpickle
from jsonfield import JSONField
from django.db import models


class GameTable(models.Model):
    STATUS_IDLE = 0
    STATUS_OPEN = 1
    STATUS_ACTIVE = 2
    STATUS_CLOSED = 3

    game_id = models.CharField(max_length=6, unique=True)
    state = JSONField(null=True, blank=True)
    prev_state = JSONField(null=True, blank=True)
    status = models.SmallIntegerField(default=STATUS_IDLE)

    @classmethod
    def get_game(cls, game_id):
        json = cls.objects.get(game_id=game_id).state
        return jsonpickle.decode(json)
