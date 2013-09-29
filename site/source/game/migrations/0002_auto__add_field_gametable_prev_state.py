# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'GameTable.prev_state'
        db.add_column(u'game_gametable', 'prev_state',
                      self.gf('jsonfield.fields.JSONField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'GameTable.prev_state'
        db.delete_column(u'game_gametable', 'prev_state')


    models = {
        u'game.gametable': {
            'Meta': {'object_name': 'GameTable'},
            'game_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '6'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'prev_state': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'state': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['game']