"""Synthetic per-filament quote tests; no private rate pack is required."""
import unittest
from decimal import Decimal

from print_quote_engine.calculator import calculate


def policy():
    return {
        'printer_catalog': {'A1': {'enabled': True}, 'Q1': {'enabled': True}},
        'material_rate_key_map': {'PLA': 'PLA_STANDARD', 'PETG': 'PETG', 'TPU': 'TPU', 'PA6-CF': 'PA6-CF'},
        'base_hourly_rates': {'PLA_STANDARD': '500', 'PETG': '1000', 'TPU': '1100', 'PA6-CF': '2000'},
        'machine_billing': {'minimum_billable_seconds': '300'},
        'size_rate_policy_map': {name: {'policy_key': 'LOW_TEMP_SIZE_RATE'} for name in ('PLA', 'PETG', 'TPU', 'PA6-CF')},
        'low_temp_size_rate_rules': [{'rank': '1', 'code': 'ALL', 'hourly_rate_multiplier': '1'}],
        'chamber_size_rate_rules': [],
        'material_pricing': {'method': 'DOMESTIC_LANDED_COST_PLUS_MARGIN_V1', 'procurement_margin_krw': '50'},
        'energy': {'unit_rate': '10'},
        'normal_multicolor_rules': [{'min_colors': '1', 'max_colors': '10', 'surcharge_rate': '0.1', 'activates_floor': False}],
        'long_print_risk_profiles': {'A1_LONG_RISK_V2': {'trigger_after_hours': '8', 'risk_rate': '0.1', 'loss_fraction_assumption': '0.1', 'activates_floor': False}},
        'conditional_floor': {'rate': '0.2'},
        'fixed_fees': {'SMALL_NOZZLE_RISK': {'amount_krw': '10'}},
        'rounding': {'final_service_supply': {'unit_krw': '100'}},
        'policy_revision': 'TEST', 'calculator_version': 'TEST', 'source_sha256': 'TEST',
    }


def quote_data():
    market = {'package_price': '1100', 'package_weight_g': '500', 'tax_included': True,
              'tax_rate': '0.1', 'inbound_shipping': '220', 'inbound_shipping_tax_included': True,
              'inbound_shipping_tax_rate': '0.1', 'reference_product': 'PLA Product', 'reference_price_id': 'pla-price'}
    other = {**market, 'package_price': '2750', 'package_weight_g': '250', 'inbound_shipping': '300',
             'inbound_shipping_tax_included': False, 'reference_product': 'PETG Product', 'reference_price_id': 'petg-price'}
    return {'printer': 'A1', 'material': 'PLA', 'duration_seconds': 3600, 'grams': '100',
            'dimensions_mm': ['10', '10', '10'], 'colors': 1, 'material_price': market,
            'energy_kwh': '0.2', 'tax_applicable': True, 'output_tax_rate': '0.1', 'extras': {},
            'material_selections': [
                {'usage_index': 0, 'material': 'PLA', 'grams': '80', 'material_price': market},
                {'usage_index': 1, 'material': 'PETG', 'grams': '20', 'material_price': other},
            ]}


class PerFilamentQuoteTests(unittest.TestCase):
    def test_distinct_package_prices_shipping_and_margin_are_prorated_separately(self):
        result = calculate(quote_data(), policy())
        amounts = {row['code']: Decimal(row['amount']) for row in result['components']}
        # PLA: 80*(1000+200+50)/500 = 200; PETG: 20*(2500+300+50)/250 = 228.
        self.assertEqual(amounts['MATERIAL'], Decimal('428'))
        self.assertEqual(amounts['MACHINE'], Decimal('500'))
        self.assertEqual(amounts['ENERGY'], Decimal('2'))
        self.assertEqual(result['subtotal'], '1000')
        self.assertEqual(result['vat'], '100')
        self.assertEqual(result['grand_total'], '1100')
        rows = result['material_breakdown']
        self.assertEqual([(r['usage_index'], r['material'], r['product'], r['grams'], r['amount']) for r in rows],
                         [(0, 'PLA', 'PLA Product', '80', '200'), (1, 'PETG', 'PETG Product', '20', '228')])
        self.assertEqual(rows[1]['material_price']['reference_price_id'], 'petg-price')
        self.assertEqual(result['trace']['material_pricing']['basis'], 'PER_FILAMENT_USAGE')
        self.assertEqual(result['trace']['material_pricing']['amount'], '428')
        self.assertIn('MULTIMATERIAL_MACHINE_POLICY_REQUIRES_REVIEW', result['manual_review_reasons'])

    def test_secondary_advanced_and_flexible_materials_keep_all_review_guards(self):
        data = quote_data()
        data['material_selections'][1]['material'] = 'PA6-CF'
        data['extras']['small_nozzle'] = True
        result = calculate(data, policy())
        self.assertIn('ENGINEERING_REQUIRES_Q1_POOL', result['manual_review_reasons'])
        self.assertIn('CF_GF_SMALL_NOZZLE_REQUIRES_MANUAL_REVIEW', result['manual_review_reasons'])
        data['material_selections'][1]['material'] = 'TPU'
        data['colors'] = 2
        self.assertIn('FLEXIBLE_MULTICOLOR_NOT_SUPPORTED', calculate(data, policy())['manual_review_reasons'])

    def test_selection_mass_is_checked_without_rescaling(self):
        data = quote_data()
        data['material_selections'][1]['grams'] = '19'
        with self.assertRaisesRegex(ValueError, 'MATERIAL_USAGE_MASS_MISMATCH'):
            calculate(data, policy())

    def test_duplicate_index_and_unknown_mass_are_rejected(self):
        data = quote_data()
        data['material_selections'][1]['usage_index'] = 0
        with self.assertRaisesRegex(ValueError, 'DUPLICATE_MATERIAL_USAGE_SELECTION'):
            calculate(data, policy())
        data = quote_data()
        data['material_selections'][1]['grams'] = None
        with self.assertRaises(ValueError):
            calculate(data, policy())

    def test_empty_selections_retain_single_material_snapshot_behavior(self):
        data = quote_data()
        data['material_selections'] = []
        result = calculate(data, policy())
        material = next(row['amount'] for row in result['components'] if row['code'] == 'MATERIAL')
        self.assertEqual(material, '250')
        self.assertNotIn('MULTIMATERIAL_MACHINE_POLICY_REQUIRES_REVIEW', result['manual_review_reasons'])


if __name__ == '__main__':
    unittest.main()
