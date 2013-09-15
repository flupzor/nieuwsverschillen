# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing M2M table for field similar_versions on 'ArticleVersion'
        db.delete_table(db.shorten_name(u'nieuwsverschillen_articleversion_similar_versions'))

        # Adding M2M table for field similar_articles on 'Article'
        m2m_table_name = db.shorten_name(u'nieuwsverschillen_article_similar_articles')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_article', models.ForeignKey(orm[u'nieuwsverschillen.article'], null=False)),
            ('to_article', models.ForeignKey(orm[u'nieuwsverschillen.article'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_article_id', 'to_article_id'])


    def backwards(self, orm):
        # Adding M2M table for field similar_versions on 'ArticleVersion'
        m2m_table_name = db.shorten_name(u'nieuwsverschillen_articleversion_similar_versions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_articleversion', models.ForeignKey(orm[u'nieuwsverschillen.articleversion'], null=False)),
            ('to_articleversion', models.ForeignKey(orm[u'nieuwsverschillen.articleversion'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_articleversion_id', 'to_articleversion_id'])

        # Removing M2M table for field similar_articles on 'Article'
        db.delete_table(db.shorten_name(u'nieuwsverschillen_article_similar_articles'))


    models = {
        u'nieuwsverschillen.article': {
            'Meta': {'object_name': 'Article'},
            'http_last_modified': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nr_downloads': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'nr_requests': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'seen_in_overview': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'similar_articles': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'similar_articles_rel_+'", 'to': u"orm['nieuwsverschillen.Article']"}),
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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