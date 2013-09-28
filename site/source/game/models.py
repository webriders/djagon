from django.db import models
from jsonfield import JSONField

import jsonpickle


class GameTable(models.Model):
    game_id = models.CharField(max_length=6, unique=True)
    state = JSONField(null=True, blank=True)
    prev_state = JSONField(null=True, blank=True)

    @classmethod
    def get_game(cls, game_id):
        json = cls.objects.get(game_id=game_id).state
        return jsonpickle.decode(json)
