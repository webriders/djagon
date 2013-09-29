import jsonpickle
from jsonfield import JSONField
from django.db import models


class GameTable(models.Model):
    game_id = models.CharField(max_length=6, unique=True)
    state = JSONField(null=True, blank=True)
    prev_state = JSONField(null=True, blank=True)

    @classmethod
    def get_game(cls, game_id):
        json = cls.objects.get(game_id=game_id).state
        return jsonpickle.decode(json)
