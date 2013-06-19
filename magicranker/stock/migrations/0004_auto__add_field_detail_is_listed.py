# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Detail.is_listed'
        db.add_column('stock_detail', 'is_listed',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Detail.is_listed'
        db.delete_column('stock_detail', 'is_listed')


    models = {
        'stock.balsheet': {
            'Meta': {'object_name': 'BalSheet'},
            'accounts_payable': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'accumulated_amortization': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'capital_surplus': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'cash_and_cash_equivalents': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'code': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stock.Detail']"}),
            'common_stock': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'deferred_long_term_asset_charges': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'deferred_long_term_liability_charges': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'goodwill': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
        'stock.detail': {
            'Meta': {'ordering': "['code']", 'object_name': 'Detail'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5'}),
            'desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'first_listed': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_listed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_listed': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'stock.pershare': {
            'Meta': {'object_name': 'PerShare'},
            'book_value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'code': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stock.Detail']"}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'earnings': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'market_cap': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pe': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'roe': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'})
        },
        'stock.pricehistory': {
            'Meta': {'object_name': 'PriceHistory'},
            'close': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'code': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stock.Detail']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'volume': ('django.db.models.fields.BigIntegerField', [], {})
        },
        'stock.sector': {
            'Meta': {'object_name': 'Sector'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['stock']