"""Mutually exclusive bed fees and frozen legacy policy behavior."""
import unittest

from print_quote_engine.calculator import calculate
from test_material_selections import policy, quote_data


def bed_policy():
    result = policy()
    result['fixed_fees']['PLATE_STANDARDIZATION'] = {'amount_krw': '777'}
    result['plate_procurement'] = {'customer_share_ratio': '0.5'}
    result['bed_fee_policy'] = {
        'mode_fees_krw': {'UNIFY': '10000', 'UNIFY_SPECIFIED': '30000', 'PURCHASE_SPECIFIED': '30000'},
        'purchase_landed_cost_share_ratio': '0.5',
        'fee_tax_basis': 'NET_SERVICE_FEE_BEFORE_OUTPUT_VAT',
        'landed_cost_basis': 'FULLY_LANDED_INCLUDING_INBOUND_SHIPPING_CUSTOMS_AND_TAXES',
    }
    return result


def bed_data(**extras):
    result = quote_data()
    result['material_selections'] = []
    result['extras'] = extras
    return result


def amounts(result):
    return {row['code']: row['amount'] for row in result['components']}


class BedFeeTests(unittest.TestCase):
    def test_unify_charges_ten_thousand_once_before_output_vat(self):
        result = calculate(bed_data(bed_mode='UNIFY'), bed_policy())
        self.assertEqual(amounts(result).get('PLATE_STANDARDIZATION'), '10000')
        self.assertEqual(result['subtotal'], '10800')
        self.assertEqual(result['vat'], '1080')
        self.assertEqual(result['grand_total'], '11880')
        self.assertEqual(result['trace']['bed_fee']['mode'], 'UNIFY')
        self.assertEqual(result['trace']['bed_fee']['amount'], '10000')
        self.assertEqual(result['trace']['bed_fee']['fee_tax_basis'], 'NET_SERVICE_FEE_BEFORE_OUTPUT_VAT')

    def test_unify_and_specify_charges_thirty_thousand_in_total(self):
        result = calculate(bed_data(bed_mode='UNIFY_SPECIFIED'), bed_policy())
        self.assertEqual(amounts(result).get('BED_UNIFICATION_SPECIFIED'), '30000')
        self.assertNotIn('PLATE_STANDARDIZATION', amounts(result))
        self.assertEqual(result['subtotal'], '30800')

    def test_purchase_uses_half_fully_landed_price_plus_thirty_thousand(self):
        result = calculate(bed_data(bed_mode='PURCHASE_SPECIFIED', bed_landed_cost='64000'), bed_policy())
        self.assertEqual(amounts(result).get('BED_PURCHASE_SPECIFIED'), '62000')
        self.assertEqual(result['subtotal'], '62800')
        self.assertEqual(result['vat'], '6280')
        self.assertEqual(result['grand_total'], '69080')
        trace = result['trace']['bed_fee']
        self.assertEqual(trace['landed_cost'], '64000')
        self.assertEqual(trace['landed_cost_share'], '32000')
        self.assertEqual(trace['selection_fee'], '30000')
        self.assertEqual(trace['landed_cost_basis'], 'FULLY_LANDED_INCLUDING_INBOUND_SHIPPING_CUSTOMS_AND_TAXES')

    def test_explicit_mode_suppresses_all_legacy_bed_flags(self):
        result = calculate(bed_data(bed_mode='UNIFY', plate_setup=True, plate_purchase='90000'), bed_policy())
        self.assertEqual(amounts(result)['PLATE_STANDARDIZATION'], '10000')
        self.assertNotIn('PLATE_PROCUREMENT', amounts(result))
        self.assertEqual(result['subtotal'], '10800')

    def test_explicit_none_charges_no_fee_even_with_legacy_flags(self):
        result = calculate(bed_data(bed_mode='NONE', plate_setup=True, plate_purchase='90000'), bed_policy())
        self.assertFalse(set(amounts(result)) & {'PLATE_STANDARDIZATION', 'PLATE_PROCUREMENT', 'BED_UNIFICATION_SPECIFIED', 'BED_PURCHASE_SPECIFIED'})
        self.assertEqual(result['subtotal'], '800')
        self.assertEqual(result['trace']['bed_fee']['mode'], 'NONE')

    def test_absent_mode_maps_legacy_setup_to_new_unify_policy(self):
        result = calculate(bed_data(plate_setup=True), bed_policy())
        self.assertEqual(amounts(result)['PLATE_STANDARDIZATION'], '10000')
        self.assertEqual(result['trace']['bed_fee']['mode'], 'UNIFY')

    def test_mapped_unify_suppresses_legacy_purchase_with_new_policy(self):
        result = calculate(bed_data(plate_setup=True, plate_purchase='90000'), bed_policy())
        self.assertEqual(amounts(result)['PLATE_STANDARDIZATION'], '10000')
        self.assertNotIn('PLATE_PROCUREMENT', amounts(result))
        self.assertEqual(result['subtotal'], '10800')

    def test_absent_mode_preserves_frozen_legacy_setup_and_purchase_amounts(self):
        frozen = bed_policy()
        frozen.pop('bed_fee_policy')
        result = calculate(bed_data(plate_setup=True, plate_purchase='90000'), frozen)
        self.assertEqual(amounts(result)['PLATE_STANDARDIZATION'], '777')
        self.assertEqual(amounts(result)['PLATE_PROCUREMENT'], '45000')
        self.assertEqual(result['subtotal'], '46600')

    def test_purchase_rejects_missing_nonpositive_and_nonexact_landed_prices(self):
        for cost in (None, '0', '-1', 'NaN', 'Infinity', True, 1.1):
            with self.subTest(cost=cost), self.assertRaises(ValueError):
                calculate(bed_data(bed_mode='PURCHASE_SPECIFIED', bed_landed_cost=cost), bed_policy())

    def test_unknown_mode_and_missing_explicit_policy_are_rejected(self):
        with self.assertRaisesRegex(ValueError, 'INVALID_BED_MODE'):
            calculate(bed_data(bed_mode='CUSTOM'), bed_policy())
        frozen = bed_policy()
        frozen.pop('bed_fee_policy')
        with self.assertRaisesRegex(ValueError, 'BED_FEE_POLICY_REQUIRED'):
            calculate(bed_data(bed_mode='UNIFY'), frozen)


if __name__ == '__main__':
    unittest.main()
