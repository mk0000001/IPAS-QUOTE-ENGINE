"""Synthetic policy values only; no operational rate pack is needed."""
import unittest
from decimal import Decimal as D

from print_quote_engine.calculator import _material_cost


class MaterialPricingTests(unittest.TestCase):
    def setUp(self):
        self.pricing = {'method': 'DOMESTIC_LANDED_COST_PLUS_MARGIN_V1', 'procurement_margin_krw': '50'}
        self.market = {'package_price': '1100', 'package_weight_g': '500', 'tax_included': True,
                       'tax_rate': '0.1', 'inbound_shipping': '220',
                       'inbound_shipping_tax_included': True, 'inbound_shipping_tax_rate': '0.1'}

    def test_landed_cost_and_margin_are_prorated_after_input_tax_removal(self):
        self.assertEqual(_material_cost(D('100'), self.market, self.pricing), D('250'))
        self.assertEqual(_material_cost(D('0'), self.market, self.pricing), D('0'))
        self.assertEqual(_material_cost(D('1000'), self.market, self.pricing), D('2500'))

    def test_no_percentage_markup_is_applied_to_new_method(self):
        self.pricing['markup_multiplier'] = '999'
        self.assertEqual(_material_cost(D('100'), self.market, self.pricing), D('250'))

    def test_shipping_tax_is_independent_of_purchase_tax(self):
        self.market['inbound_shipping_tax_included'] = False
        self.assertEqual(_material_cost(D('100'), self.market, self.pricing), D('254'))
        self.market['tax_included'] = False
        self.assertEqual(_material_cost(D('100'), self.market, self.pricing), D('274'))

    def test_omitted_inbound_shipping_means_zero(self):
        self.market.pop('inbound_shipping')
        self.assertEqual(_material_cost(D('100'), self.market, self.pricing), D('210'))

    def test_old_policy_snapshot_retains_original_multiplier_formula(self):
        legacy = {'markup_multiplier': '1.3'}
        self.assertEqual(_material_cost(D('100'), self.market, legacy), D('260'))

    def test_invalid_shipping_margin_weight_and_method_are_rejected(self):
        for value in ('-1', 'NaN', 'Infinity', True, 1.2):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    _material_cost(D('100'), {**self.market, 'inbound_shipping': value}, self.pricing)
                with self.assertRaises(ValueError):
                    _material_cost(D('100'), self.market, {**self.pricing, 'procurement_margin_krw': value})
        with self.assertRaises(ValueError):
            _material_cost(D('100'), {**self.market, 'package_weight_g': '0'}, self.pricing)
        with self.assertRaisesRegex(ValueError, 'UNKNOWN_MATERIAL_PRICING_METHOD'):
            _material_cost(D('100'), self.market, {**self.pricing, 'method': 'TYPO'})


if __name__ == '__main__':
    unittest.main()
