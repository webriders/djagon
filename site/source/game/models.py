from django.db import models
from jsonfield import JSONField


class GameTable(models.Model):
    game_id = models.CharField(max_length=6, unique=True)
    state = JSONField(null=True, blank=True)

