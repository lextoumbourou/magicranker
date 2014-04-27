import unittest

from app.helpers import process_methods

class HelperTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_process_methods(self):
        data = {
            'rank_methods': [{
                'name': 'roe',
                'is_selected': True,
                'max': 0.70
            },{
                'name': 'pe',
                'is_selected': False
            }],
            'filter_methods': [],
            'limit': '100'
        }
        rank_methods, filter_methods, limit = process_methods(data)
        assert rank_methods[0]['name'] == 'roe'
        assert len(filter_methods) == 0
        assert limit == 100
