# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Detail'
        db.create_table(u'stock_detail', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=5)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('desc', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('last_updated', self.gf('django.db.models.fields.DateField')(null=True)),
            ('is_listed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'stock', ['Detail'])

        # Adding model 'Sector'
        db.create_table(u'stock_sector', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=60)),
        ))
        db.send_create_signal(u'stock', ['Sector'])

        # Adding model 'PerShare'
        db.create_table(u'stock_pershare', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stock.Detail'])),
            ('date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('earnings', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2, blank=True)),
            ('roe', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2, blank=True)),
            ('book_value', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2, blank=True)),
            ('pe', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2, blank=True)),
            ('market_cap', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'stock', ['PerShare'])

        # Adding model 'BalSheet'
        db.create_table(u'stock_balsheet', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stock.Detail'])),
            ('period_ending', self.gf('django.db.models.fields.DateField')(null=True)),
            ('cash_and_cash_equivalents', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
            ('short_term_investments', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
            ('net_receivables', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
            ('inventory', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
            ('other_current_assets', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
            ('total_current_assets', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
            ('long_term_investments', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
            ('property_plant_and_equipment', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
            ('goodwill', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
            ('intangible_assets', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
            ('accumulated_amortization', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
            ('other_assets', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
            ('deferred_long_term_asset_charges', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
            ('total_assets', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
            ('accounts_payable', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
            ('short_current_long_term_debt', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
            ('other_current_liabilities', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
            ('total_current_liabilities', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
            ('long_term_debt', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
            ('other_liabilities', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
            ('deferred_long_term_liability_charges', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
            ('minority_interest', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
            ('negative_goodwill', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
            ('total_liabilities', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
            ('stockholders_equity', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
            ('misc_stocks_options_warrants', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
            ('redeemable_preferred_stock', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
            ('preferred_stock', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
            ('common_stock', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
            ('retained_earnings', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
            ('treasury_stock', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
            ('capital_surplus', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
            ('other_stockholder_equity', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
            ('total_stockholder_equity', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
            ('net_tangible_assets', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
        ))
        db.send_create_signal(u'stock', ['BalSheet'])

        # Adding model 'PriceHistory'
        db.create_table(u'stock_pricehistory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stock.Detail'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('close', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('volume', self.gf('django.db.models.fields.BigIntegerField')()),
        ))
        db.send_create_signal(u'stock', ['PriceHistory'])


    def backwards(self, orm):
        # Deleting model 'Detail'
        db.delete_table(u'stock_detail')

        # Deleting model 'Sector'
        db.delete_table(u'stock_sector')

        # Deleting model 'PerShare'
        db.delete_table(u'stock_pershare')

        # Deleting model 'BalSheet'
        db.delete_table(u'stock_balsheet')

        # Deleting model 'PriceHistory'
        db.delete_table(u'stock_pricehistory')


    models = {
        u'stock.balsheet': {
            'Meta': {'object_name': 'BalSheet'},
            'accounts_payable': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'accumulated_amortization': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'capital_surplus': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'cash_and_cash_equivalents': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'code': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stock.Detail']"}),
            'common_stock': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'deferred_long_term_asset_charges': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'deferred_long_term_liability_charges': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'goodwill': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intangible_assets': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'inventory': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'long_term_debt': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'long_term_investments': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'minority_interest': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'misc_stocks_options_warrants': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'negative_goodwill': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'net_receivables': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'net_tangible_assets': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'other_assets': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'other_current_assets': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'other_current_liabilities': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'other_liabilities': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'other_stockholder_equity': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'period_ending': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'preferred_stock': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'property_plant_and_equipment': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'redeemable_preferred_stock': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'retained_earnings': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'short_current_long_term_debt': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'short_term_investments': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'stockholders_equity': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'total_assets': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'total_current_assets': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'total_current_liabilities': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'total_liabilities': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'total_stockholder_equity': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'treasury_stock': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'})
        },
        u'stock.detail': {
            'Meta': {'ordering': "['code']", 'object_name': 'Detail'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5'}),
            'desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_listed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_updated': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'stock.pershare': {
            'Meta': {'object_name': 'PerShare'},
            'book_value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'code': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stock.Detail']"}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'earnings': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'market_cap': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pe': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'roe': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'})
        },
        u'stock.pricehistory': {
            'Meta': {'object_name': 'PriceHistory'},
            'close': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'code': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stock.Detail']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'volume': ('django.db.models.fields.BigIntegerField', [], {})
        },
        u'stock.sector': {
            'Meta': {'object_name': 'Sector'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['stock']