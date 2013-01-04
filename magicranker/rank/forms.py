from django import forms

from lib.ranker import RankMethod, FilterMethod

class RankForm(forms.Form):
    ORDER_CHOICES = (('1','1'),
                     ('2','2'),
                     ('3','3'),
                     ('4','4'))
    # Ranks
    rank_roe = forms.BooleanField(required=False)
    rank_roe_average = forms.ChoiceField(
        required=False, choices=(
            ('0','0'),('2','2'),('3','3'),('5','5'),('10','10'),))
    rank_roe_max = forms.ChoiceField(
        required=False, choices=(
            ('', 'infinity'),('1.0', '100'),('0.70','70'),
            ('0.50','50'),('0.30','30')))

    rank_pe = forms.BooleanField(required=False)
    rank_pe_min = forms.ChoiceField(
        required=False, choices=(
            ('0', ''),('2', '2'),('3','3'),
            ('5','5'),('10','10')))

    rank_market_cap = forms.BooleanField(required=False)
    rank_debt_per = forms.BooleanField(required=False)

    # Filters
    filt_roe = forms.BooleanField(required=False)
    filt_roe_min = forms.IntegerField(min_value=0, required=False)
    filt_roe_max = forms.IntegerField(required=False)

    filt_pe = forms.BooleanField(required=False)
    filt_pe_min = forms.IntegerField(required=False)
    filt_pe_max = forms.IntegerField(required=False)

    filt_market_cap = forms.BooleanField(required=False)
    filt_market_cap_min = forms.ChoiceField(
        required=False, choices=(
            ('0', '0'),('250000000', '250'),('5000000','500'),
            ('1000000000','1000'),))

    filt_debt_per = forms.BooleanField(required=False)
    filt_debt_per = forms.IntegerField(required=False)

    # Limit
    limit = forms.ChoiceField(
        required=False, choices=(('50','50'),('30','30'),('10','10')))

    def get_rank_methods(self):
        output = [] 
        if self.cleaned_data.get('rank_roe'):
            # Roe is ordered from highest to lowest
            output.append(RankMethod(
                name='roe', 
                average=self.cleaned_data.get('rank_roe_avg', 0), 
                min=self.cleaned_data.get('rank_roe_min', 0.05),
                max=self.cleaned_data.get('rank_roe_max', 0.70), 
                order='-roe'))
        if self.cleaned_data.get('rank_pe'):
              # Pe is ordered from lowest to highest
              output.append(RankMethod(
                  name='pe', 
                  min=self.cleaned_data.get('rank_pe_min', 0),
                  max=self.cleaned_data.get('rank_pe_max'), 
                  order='pe'))
        if self.cleaned_data.get('market_cap_rank'):
            # Market Cap is ordered from highest to lowest
            output.append(RankMethod(
                name='market_cap', 
                min=self.cleaned_data.get('market_cap_min'),
                order='market_cap'))
        if self.cleaned_data.get('debt_per_rank'):
            # Debt is ordered from lowest to highest
            output.append(Rank_Method(
                name='debt_per', 
                max=self.cleaned_data.get('debt_per_max'),
                order='-debt_per'))
        return output

    def get_filter_methods(self):
        output = []
        if self.cleaned_data.get('filter_roe'):
            # Roe is ordered from highest to lowest
            output.append(Filter_Method(
                name='roe', min=cd['roe_rank_min'],
                max=cd['roe_rank_max']))
        if self.cleaned_data.get('filter_pe'):
              # Pe is ordered from lowest to highest
              output.append(Filter_Method(
                  name='pe', min=cd['pe_rank_min'],
                  max=cd['pe_rank_max']))
        if self.cleaned_data.get('filter_market_cap'):
            # Market Cap is ordered from highest to lowest
            output.append(Filter_Method(
                name='market_cap', min=cd['market_cap_min'],
                order='market_cap'))
        if self.cleaned_data.get('filter_debt_per'):
            # Debt is ordered from lowest to highest
            output.append(Filter_Method(
                name='debt_per', max=cd['debt_per_max'],
                order='-debt_per'))
        return output


class ContactForm(forms.Form):
    subject = forms.CharField()
    email = forms.EmailField(required=False)
    message = forms.CharField()
