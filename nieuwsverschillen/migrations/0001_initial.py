# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Source'
        db.create_table(u'nieuwsverschillen_source', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('parser_path', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'nieuwsverschillen', ['Source'])

        # Adding model 'Article'
        db.create_table(u'nieuwsverschillen_article', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['nieuwsverschillen.Source'])),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255)),
            ('url', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('nr_requests', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('nr_downloads', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('seen_in_overview', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('http_last_modified', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'nieuwsverschillen', ['Article'])

        # Adding model 'ArticleVersion'
        db.create_table(u'nieuwsverschillen_articleversion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('article', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['nieuwsverschillen.Article'])),
            ('http_download_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('http_content', self.gf('django.db.models.fields.TextField')()),
            ('http_headers', self.gf('json_field.fields.JSONField')(default=u'null')),
            ('article_title', self.gf('django.db.models.fields.TextField')()),
            ('article_content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'nieuwsverschillen', ['ArticleVersion'])

        # Adding M2M table for field similar_versions on 'ArticleVersion'
        m2m_table_name = db.shorten_name(u'nieuwsverschillen_articleversion_similar_versions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_articleversion', models.ForeignKey(orm[u'nieuwsverschillen.articleversion'], null=False)),
            ('to_articleversion', models.ForeignKey(orm[u'nieuwsverschillen.articleversion'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_articleversion_id', 'to_articleversion_id'])


    def backwards(self, orm):
        # Deleting model 'Source'
        db.delete_table(u'nieuwsverschillen_source')

        # Deleting model 'Article'
        db.delete_table(u'nieuwsverschillen_article')

        # Deleting model 'ArticleVersion'
        db.delete_table(u'nieuwsverschillen_articleversion')

        # Removing M2M table for field similar_versions on 'ArticleVersion'
        db.delete_table(db.shorten_name(u'nieuwsverschillen_articleversion_similar_versions'))


    models = {
        u'nieuwsverschillen.article': {
            'Meta': {'object_name': 'Article'},
            'http_last_modified': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nr_downloads': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'nr_requests': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'seen_in_overview': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['nieuwsverschillen.Source']"}),
            'url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'nieuwsverschillen.articleversion': {
            'Meta': {'object_name': 'ArticleVersion'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['nieuwsverschillen.Article']"}),
            'article_content': ('django.db.models.fields.TextField', [], {}),
            'article_title': ('django.db.models.fields.TextField', [], {}),
            'http_content': ('django.db.models.fields.TextField', [], {}),
            'http_download_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'http_headers': ('json_field.fields.JSONField', [], {'default': "u'null'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'similar_versions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'similar_versions_rel_+'", 'to': u"orm['nieuwsverschillen.ArticleVersion']"})
        },
        u'nieuwsverschillen.source': {
            'Meta': {'object_name': 'Source'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parser_path': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['nieuwsverschillen']