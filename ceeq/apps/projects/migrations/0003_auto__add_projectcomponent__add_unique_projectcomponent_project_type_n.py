# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ProjectComponent'
        db.create_table(u'projects_projectcomponent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.ProjectType'])),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
            ('weight', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=3, decimal_places=2)),
        ))
        db.send_create_signal(u'projects', ['ProjectComponent'])

        # Adding unique constraint on 'ProjectComponent', fields ['project_type', 'name', 'weight']
        db.create_unique(u'projects_projectcomponent', ['project_type_id', 'name', 'weight'])

        # Adding model 'ProjectType'
        db.create_table(u'projects_projecttype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', unique=True, max_length=50)),
        ))
        db.send_create_signal(u'projects', ['ProjectType'])

        # Adding field 'Project.project_type'
        db.add_column(u'projects_project', 'project_type',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['projects.ProjectType']),
                      keep_default=False)


    def backwards(self, orm):
        # Removing unique constraint on 'ProjectComponent', fields ['project_type', 'name', 'weight']
        db.delete_unique(u'projects_projectcomponent', ['project_type_id', 'name', 'weight'])

        # Deleting model 'ProjectComponent'
        db.delete_table(u'projects_projectcomponent')

        # Deleting model 'ProjectType'
        db.delete_table(u'projects_projecttype')

        # Deleting field 'Project.project_type'
        db.delete_column(u'projects_project', 'project_type_id')


    models = {
        u'projects.frameworkparameter': {
            'Meta': {'object_name': 'FrameworkParameter'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parameter': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'value': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '3', 'decimal_places': '2'})
        },
        u'projects.project': {
            'Meta': {'object_name': 'Project'},
            'accessibility': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'accuracy': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'complete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'efficiency': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'functional_security': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interoperability': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'jira_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'jira_version': ('django.db.models.fields.CharField', [], {'default': "'All Versions'", 'max_length': '200'}),
            'maintainability': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'portability': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'project_type': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['projects.ProjectType']"}),
            'reliability': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'score': ('django.db.models.fields.DecimalField', [], {'default': '109', 'max_digits': '5', 'decimal_places': '2'}),
            'suitability': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'technical_security': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'usability': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        u'projects.projectcomponent': {
            'Meta': {'unique_together': "(('project_type', 'name', 'weight'),)", 'object_name': 'ProjectComponent'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'project_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.ProjectType']"}),
            'weight': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '3', 'decimal_places': '2'})
        },
        u'projects.projectcomponentsdefectsdensity': {
            'Meta': {'ordering': "['created', 'version']", 'object_name': 'ProjectComponentsDefectsDensity'},
            'application': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '5', 'decimal_places': '3'}),
            'ceeq': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '5', 'decimal_places': '3'}),
            'ceeq_closed': ('django.db.models.fields.DecimalField', [], {'default': '10', 'max_digits': '5', 'decimal_places': '3'}),
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'cxp': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '5', 'decimal_places': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'platform': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '5', 'decimal_places': '3'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.Project']"}),
            'reports': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '5', 'decimal_places': '3'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'voice_slots': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '5', 'decimal_places': '3'})
        },
        u'projects.projecttype': {
            'Meta': {'object_name': 'ProjectType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '50'})
        }
    }

    complete_apps = ['projects']