import unittest
from unittest.mock import patch

from print_quote_engine.batch import calculate_batch


class BatchQuoteTests(unittest.TestCase):
    def test_each_file_is_calculated_in_order_and_failure_is_isolated(self):
        items=[{'source_file_version_id':'a'},{'source_file_version_id':'b'},{'source_file_version_id':'c'}]
        with patch('print_quote_engine.batch.calculate',side_effect=[{'grand_total':'10000'},ValueError('BAD_PRICE'),{'grand_total':'30000'}]) as mocked:
            result=calculate_batch(items,{'policy_revision':'test'})
        self.assertEqual(result['requested'],3)
        self.assertEqual(result['succeeded'],2)
        self.assertEqual(result['failed'],1)
        self.assertEqual(result['items'][0],{'index':0,'status':'SUCCEEDED','result':{'grand_total':'10000'}})
        self.assertEqual(result['items'][1],{'index':1,'status':'FAILED','error_code':'BAD_PRICE'})
        self.assertEqual(result['items'][2]['index'],2)
        self.assertEqual(mocked.call_count,3)

    def test_batch_rejects_empty_and_oversized_requests(self):
        for items in ([],[{}]*51):
            with self.subTest(size=len(items)),self.assertRaises(ValueError):
                calculate_batch(items,{})


if __name__=='__main__':
    unittest.main()
