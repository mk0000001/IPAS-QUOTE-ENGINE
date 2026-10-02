"""Explicit slicer model time must not inherit a different historical warm-up time."""
import unittest
from decimal import Decimal

from print_quote_engine.energy import estimate_energy


class ExplicitModelEnergyTests(unittest.TestCase):
    def policy(self):
        return {'energy_model': {'geometries': {'TEST': {'bed_mm': [250, 250], 'height_mm': 250}}},
                'energy_telemetry': {'collected_at_ts': 2000,
                    'profiles': {'TEST': [{'mean_w': 200, 'bed_c': 60, 'nozzle_c': 220, 'sample_hours': 5,
                                           'auxiliary_loads_included': ['AMS_DRYING_DURING_PRINT']}]},
                    'preparation': {'TEST': {'status': 'READY', 'method': 'TEST_INTEGRATION', 'sessions': [
                        {'end_ts': 1000, 'energy_wh': 30, 'seconds': 500, 'bed_c': 60, 'nozzle_c': 220},
                        {'end_ts': 1900, 'energy_wh': 30, 'seconds': 500, 'bed_c': 60, 'nozzle_c': 220}]}}}}

    def data(self, scope='TOTAL_WITH_PREPARATION', model='3600'):
        settings = {'bed_temp': '60', 'nozzle_temp': '220', 'duration_scope': scope,
                    'energy_condition_sources': {'model_print_seconds': 'GCODE_MODEL_TIME_HEADER'}}
        if model is not None:
            settings['model_print_seconds'] = model
        return {'printer': 'TEST', 'material': 'PLA', 'grams': '50', 'duration_seconds': 4200,
                'process_settings': settings}

    def test_explicit_model_time_wins_over_different_historical_preparation_duration(self):
        result = estimate_energy(self.data(), self.policy())
        # Slicer model 3600 s and history preparation 500 s are independent.
        self.assertEqual(Decimal(result['kwh']), Decimal('.23'))
        self.assertEqual(Decimal(result['pricing_print_seconds']), Decimal(3600))
        self.assertEqual(result['pricing_print_seconds_basis'], 'SLICER_EXPLICIT_MODEL_TIME')
        self.assertEqual(result['preparation_method'], 'HA_MATCHED_PREPARATION_HISTORY')
        self.assertEqual(result['accessory_energy_accounting'], 'INCLUDED_IN_REFERENCE_METER_TOTAL')

    def test_missing_model_time_retains_historical_duration_difference(self):
        result = estimate_energy(self.data(model=None), self.policy())
        self.assertEqual(Decimal(result['pricing_print_seconds']), Decimal(3700))
        self.assertAlmostEqual(float(result['kwh']), .23555555555555556)
        self.assertEqual(result['pricing_print_seconds_basis'], 'HISTORICAL_PREPARATION_DURATION_DIFFERENCE')

    def test_invalid_or_uncorroborated_model_time_cannot_reduce_priced_print_duration(self):
        for value in ('NaN', 'Infinity', '-1', '4201', '1.5', '3600 extra', True, 3600.0, '1000000000001'):
            with self.subTest(value=value):
                result = estimate_energy(self.data(model=value), self.policy())
                self.assertEqual(Decimal(result['pricing_print_seconds']), Decimal(3700))
                self.assertEqual(result['pricing_print_seconds_basis'], 'HISTORICAL_PREPARATION_DURATION_DIFFERENCE')
        data = self.data()
        data['process_settings']['energy_condition_sources'] = {}
        result = estimate_energy(data, self.policy())
        self.assertEqual(Decimal(result['pricing_print_seconds']), Decimal(3700))

    def test_unknown_or_print_only_scope_ignores_total_scope_model_override(self):
        for scope, basis in (('UNKNOWN', 'UNRESOLVED_FULL_INPUT_DURATION'), ('PRINT_ONLY', 'INPUT_PRINT_ONLY_DURATION')):
            with self.subTest(scope=scope):
                result = estimate_energy(self.data(scope, '1'), self.policy())
                self.assertEqual(Decimal(result['pricing_print_seconds']), Decimal(4200))
                self.assertEqual(result['pricing_print_seconds_basis'], basis)

    def test_zero_model_time_can_be_all_preparation_without_printing_energy(self):
        result = estimate_energy(self.data(model='0'), self.policy())
        self.assertEqual(Decimal(result['kwh']), Decimal('.03'))
        self.assertEqual(Decimal(result['pricing_print_seconds']), Decimal(0))

    def test_known_model_time_is_retained_when_preparation_is_only_theoretical(self):
        policy = self.policy()
        policy['energy_telemetry']['preparation'] = {}
        result = estimate_energy(self.data(), policy)
        self.assertEqual(Decimal(result['pricing_print_seconds']), Decimal(3600))
        self.assertEqual(result['pricing_print_seconds_basis'], 'SLICER_EXPLICIT_MODEL_TIME')
        self.assertEqual(result['preparation_method'], 'THEORETICAL_COLD_START')
        self.assertGreater(result['warmup_wh'], 0)


if __name__ == '__main__':
    unittest.main()
