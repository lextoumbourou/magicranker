import unittest

from app.helpers import process_methods, get_filtered_data

class HelperTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_process_methods(self):
        data = {
            'rank_methods': [{
                'name':'roe',
                'max': {
                    'changeable':True,
                    'value': 0.7,
                },
                'average':{
                    'changeable':True,
                    'value': 1,
                 },
                'is_selected':True,
                'ascending':False,
                'human_name':u'Return On Equity'
            }],
            'filter_methods': [],
            'limit': '100'
        }
        rank_methods, filter_methods, limit = process_methods(data)
        assert rank_methods[0]['name'] == 'roe'
        assert rank_methods[0]['max'] == 0.7
        assert len(filter_methods) == 0
        assert limit == 100
