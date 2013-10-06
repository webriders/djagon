from jsonfield import JSONField
from django.db import models


class StoredGame(models.Model):
    STATE_IDLE = 0
    STATE_OPEN = 1
    STATE_ACTIVE = 2
    STATE_CLOSED = 3

    game_id = models.CharField(max_length=6, unique=True)
    game_state = models.SmallIntegerField(default=STATE_IDLE)
    game_jsoned = JSONField(null=True, blank=True)
