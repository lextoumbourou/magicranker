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
        
    filter_debt_per = forms.BooleanField(required=False)
    filter_debt_per = forms.IntegerField(required=False)

    # Limit
    limit = forms.ChoiceField(
        required=False, choices=(('50','50'),('30','30'),('10','10')))

    def get_rank_methods(self):
        output = [] 
        if self.cleaned_data.get('rank_roe'):
            # Roe is ordered from highest to lowest
            output.append(RankMethod(
                name='roe', 
                min=self.cleaned_data.get('rank_roe_min', 0.05),
                max=self.cleaned_data.get('rank_roe_max', 0.70), 
                average=self.cleaned_data.get('rank_roe_avg', 0), 
                desc=True))
        #if self.cleaned_data.get('rank_pe'):
        #    print "For some reason I'm here"
        #    # Pe is ordered from lowest to highest
        #    output.append(RankMethod(
        #        name='pe', 
        #        min=self.cleaned_data.get('rank_pe_min', 0),
        #        max=self.cleaned_data.get('rank_pe_max')))
        if self.cleaned_data.get('rank_market_cap'):
            # Market Cap is ordered from highest to lowest
            output.append(RankMethod(
                name='market_cap', 
                min=self.cleaned_data.get('rank_market_cap_min'),
                order='market_cap'))
        if self.cleaned_data.get('rank_debt'):
            # Debt is ordered from lowest to highest
            output.append(RankMethod(
                name='debt_per', 
                max=self.cleaned_data.get('rank_debt_max'),
                order='-debt_per'))
        return output

    def get_filter_methods(self):
        output = []
        cd = self.cleaned_data
        if self.cleaned_data.get('filter_roe'):
            cd = self.cleaned_data
            # Roe is ordered from highest to lowest
            output.append(FilterMethod(
                name='roe', min=cd['roe_rank_min'],
                max=cd['roe_rank_max']))
        if self.cleaned_data.get('filter_pe'):
              # Pe is ordered from lowest to highest
              output.append(FilterMethod(
                  name='pe', min=cd['pe_rank_min'],
                  max=cd['pe_rank_max']))
        if self.cleaned_data.get('filter_market_cap'):
            # Market Cap is ordered from highest to lowest
            output.append(FilterMethod(
                name='market_cap', min=self.cleaned_data['filter_market_cap_min']))
        if self.cleaned_data.get('filter_debt'):
            # Debt is ordered from lowest to highest
            output.append(FilterMethod(
                name='debt_per', max=self.cleaned_data['filter_debt_max']))
        return output


class ContactForm(forms.Form):
    subject = forms.CharField()
    email = forms.EmailField(required=False)
    message = forms.CharField()
