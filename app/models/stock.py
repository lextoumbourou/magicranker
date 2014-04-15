from decimal import Decimal

from .. import db
from . import CRUDMixin

class Detail(models.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(5), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(), nullable=False, blank=True)
    first_listed = db.Column(db.DateTime)
    last_listed = db.Column(db.DateTime)
    is_listed = db.Column(db.Integer)

class Sector(models.Model):
    category = db.Column(db.String(60))

class PerShare(models.Model):
    date = db.Column(db.DateTime)
    earnings = db.Column(db.Float(asdecimal=True)
    roe = db.Column(db.Float(asdecimal=True))
    book_value = db.Column(db.Float(asdecimal=True)
    pe = db.Column(db.Float(asdecimal=True))
    market_cap = db.Column(db.BigInteger)
    shares_outstanding = db.Column(db.BigInteger)
    total_debt_ratio = db.Column(db.Float(asdecimal=True)

    code_id = db.Column(db.Integer, db.ForeignKey('detail.id'))
    code = db.relationship('Detail', backref=db.backref('pershares'))

class BalSheet(models.Model):
    period_ending = db.Column(db.DateTime)
    cash_and_cash_equivalents = db.Column(db.BigInteger)
    short_term_investments = db.Column(db.BigInteger)
    net_receivables = db.Column(db.BigInteger)
    inventory = db.Column(db.BigInteger)
    other_current_assets = db.Column(db.BigInteger)
    total_current_assets = db.Column(db.BigInteger)
    long_term_investments = db.Column(db.BigInteger)
    property_plant_and_equipment = db.Column(db.BigInteger)
    goodwill = db.Column(db.BigInteger)
    intangible_assets = db.Column(db.BigInteger)
    accumulated_amortization = db.Column(db.BigInteger)
    other_assets = db.Column(db.BigInteger)
    deferred_long_term_asset_charges = db.Column(db.BigInteger)
    total_assets = db.Column(db.BigInteger)
    accounts_payable = db.Column(db.BigInteger)
    short_current_long_term_debt = db.Column(db.BigInteger)
    other_current_liabilities = db.Column(db.BigInteger)
    total_current_liabilities = db.Column(db.BigInteger)
    long_term_debt = db.Column(db.BigInteger)
    other_liabilities = db.Column(db.BigInteger)
    deferred_long_term_liability_charges = db.Column(db.BigInteger)
    minority_interest = db.Column(db.BigInteger)
    negative_goodwill = db.Column(db.BigInteger)
    total_liabilities = db.Column(db.BigInteger)
    stockholders_equity = db.Column(db.BigInteger)
    misc_stocks_options_warrants = db.Column(db.BigInteger)
    redeemable_preferred_stock = db.Column(db.BigInteger)
    preferred_stock = db.Column(db.BigInteger)
    common_stock = db.Column(db.BigInteger)
    retained_earnings = db.Column(db.BigInteger)
    treasury_stock = db.Column(db.BigInteger)
    capital_surplus = db.Column(db.BigInteger)
    other_stockholder_equity = db.Column(db.BigInteger)
    total_stockholder_equity = db.Column(db.BigInteger)
    net_tangible_assets = db.Column(db.BigInteger)

    code_id = db.Column(db.Integer, db.ForeignKey('detail.id'))
    code = db.relationship('Detail', backref=db.backref('pricehistorys'))

    def _get_total_debt_ratio(self):
        if self.total_assets and self.total_liabilities:
            return float(self.total_assets) / self.total_liabilities

    total_debt_ratio = (_get_total_debt_ratio)


class PriceHistory(models.Model):
    date = db.Column(db.DateTime)
    close = db.Column(db.Float(asdecimal=True)
    volume = db.Column(db.BigInteger)

    code_id = db.Column(db.Integer, db.ForeignKey('detail.id'))
    code = db.relationship('Detail', backref=db.backref('pricehistorys'))
