from django import forms

from magicranker.rank.Ranker import RankMethod, FilterMethod

class RankForm(forms.Form):
    ORDER_CHOICES = (('1','1'),
                     ('2','2'),
                     ('3','3'),
                     ('4','4'))
    # Ranks
    rank_roe = forms.BooleanField(required=False)
    rank_roe_avg = forms.IntegerField(
        min_value=1, max_value=10, initial=1, required=False)
    rank_roe_max = forms.DecimalField(
        min_value=0, max_value=1, initial=0.70, required=False)

    rank_pe = forms.BooleanField(required=False)
    rank_pe_min = forms.IntegerField(
        min_value=0, max_value=10, initial=0, required=False)

    rank_market_cap = forms.BooleanField(required=False)
    rank_debt_per = forms.BooleanField(required=False)

    # Filters
    filter_roe = forms.BooleanField(required=False)
    filter_roe_min = forms.IntegerField(min_value=0, required=False)
    filter_roe_max = forms.IntegerField(required=False)

    filter_pe = forms.BooleanField(required=False)
    filter_pe_min = forms.IntegerField(min_value=0, required=False)
    filter_pe_max = forms.IntegerField(min_value=0, required=False)

    filter_market_cap = forms.BooleanField(required=False)
    filter_market_cap_min = forms.IntegerField(
        min_value=0, max_value=1000000000, initial=0)
        
    filter_debt = forms.BooleanField(required=False)
    filter_debt_max = forms.DecimalField(required=False)

    # Limit
    limit = forms.ChoiceField(
        required=False, choices=(('50','50'),('30','30'),('10','10')))

    
class ContactForm(forms.Form):
    subject = forms.CharField()
    email = forms.EmailField(required=False)
    message = forms.CharField()
