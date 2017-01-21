from django.db import models
from django_pandas.managers import DataFrameManager


class Detail(models.Model):

    """Store core information about listed companies."""

    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    first_listed = models.DateField(null=True)
    last_listed = models.DateField(null=True)
    is_listed = models.BooleanField()

    class Meta:
        ordering = ['code']

    def __unicode__(self):
        return self.code


class Sector(models.Model):

    """Provide sectors for categorizing companies."""

    category = models.CharField(max_length=60)

    def __unicode__(self):
        return self.category


class PerShare(models.Model):

    """Per share metrics for listed companies."""

    code = models.ForeignKey(Detail)
    date = models.DateField(null=True)
    year = models.IntegerField()
    earnings = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    roe = models.DecimalField(
        null=True, blank=True, max_digits=10, decimal_places=2)
    book_value = models.DecimalField(
        null=True, blank=True, max_digits=10, decimal_places=2)
    pe = models.DecimalField(
        null=True, blank=True, max_digits=10, decimal_places=2)
    market_cap = models.BigIntegerField(null=True, blank=True)
    shares_outstanding = models.BigIntegerField(null=True, blank=True)
    total_debt_ratio = models.DecimalField(
        null=True, blank=True, max_digits=10, decimal_places=2)

    objects = DataFrameManager()

    def __unicode__(self):
        return '{0} - {1}'.format(self.code.code, self.date)


class BalSheet(models.Model):

    """Store balance sheet metrics for listed companies."""

    code = models.ForeignKey(Detail)
    period_ending = models.DateField(null=True)
    cash_and_cash_equivalents = models.BigIntegerField(null=True)
    short_term_investments = models.BigIntegerField(null=True)
    net_receivables = models.BigIntegerField(null=True)
    inventory = models.BigIntegerField(null=True)
    other_current_assets = models.BigIntegerField(null=True)
    total_current_assets = models.BigIntegerField(null=True)
    long_term_investments = models.BigIntegerField(null=True)
    property_plant_and_equipment = models.BigIntegerField(null=True)
    goodwill = models.BigIntegerField(null=True)
    intangible_assets = models.BigIntegerField(null=True)
    accumulated_amortization = models.BigIntegerField(null=True)
    other_assets = models.BigIntegerField(null=True)
    deferred_long_term_asset_charges = models.BigIntegerField(null=True)
    total_assets = models.BigIntegerField(null=True)
    accounts_payable = models.BigIntegerField(null=True)
    short_current_long_term_debt = models.BigIntegerField(null=True)
    other_current_liabilities = models.BigIntegerField(null=True)
    total_current_liabilities = models.BigIntegerField(null=True)
    long_term_debt = models.BigIntegerField(null=True)
    other_liabilities = models.BigIntegerField(null=True)
    deferred_long_term_liability_charges = models.BigIntegerField(null=True)
    minority_interest = models.BigIntegerField(null=True)
    negative_goodwill = models.BigIntegerField(null=True)
    total_liabilities = models.BigIntegerField(null=True)
    stockholders_equity = models.BigIntegerField(null=True)
    misc_stocks_options_warrants = models.BigIntegerField(null=True)
    redeemable_preferred_stock = models.BigIntegerField(null=True)
    preferred_stock = models.BigIntegerField(null=True)
    common_stock = models.BigIntegerField(null=True)
    retained_earnings = models.BigIntegerField(null=True)
    treasury_stock = models.BigIntegerField(null=True)
    capital_surplus = models.BigIntegerField(null=True)
    other_stockholder_equity = models.BigIntegerField(null=True)
    total_stockholder_equity = models.BigIntegerField(null=True)
    net_tangible_assets = models.BigIntegerField(null=True)

    def _get_total_debt_ratio(self):
        if self.total_assets and self.total_liabilities:
            return float(self.total_assets) / self.total_liabilities

    total_debt_ratio = (_get_total_debt_ratio)

    def __unicode__(self):
        return '{0} {1}'.format(self.code.code, str(self.period_ending))


class PriceHistory(models.Model):

    """Historical price history for listed companies."""

    code = models.ForeignKey(Detail)
    date = models.DateField()
    close = models.DecimalField(max_digits=5, decimal_places=2)
    volume = models.BigIntegerField()

    def __unicode__(self):
        return '{0} {1}'.format(self.code, unicode(self.date))
