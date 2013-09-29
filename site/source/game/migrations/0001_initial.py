# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'GameTable'
        db.create_table(u'game_gametable', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=6)),
            ('state', self.gf('jsonfield.fields.JSONField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'game', ['GameTable'])


    def backwards(self, orm):
        # Deleting model 'GameTable'
        db.delete_table(u'game_gametable')


    models = {
        u'game.gametable': {
            'Meta': {'object_name': 'GameTable'},
            'game_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '6'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['game']