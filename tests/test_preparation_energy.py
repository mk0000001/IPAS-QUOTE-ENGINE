import unittest
from decimal import Decimal
from print_quote_engine.energy import estimate_energy


class PreparationEnergyTests(unittest.TestCase):
    def policy(self):
        return {'energy_model':{'geometries':{'TEST':{'bed_mm':[250,250],'height_mm':250}}},
            'energy_telemetry':{'collected_at_ts':2000,'profiles':{'TEST':[{'mean_w':200,'bed_c':60,'nozzle_c':220,'sample_hours':5}]},
                'preparation':{'TEST':{'status':'READY','method':'TEST_INTEGRATION','sessions':[
                    {'end_ts':1000,'energy_wh':30,'seconds':600,'bed_c':60,'nozzle_c':220},
                    {'end_ts':1900,'energy_wh':30,'seconds':600,'bed_c':60,'nozzle_c':220}]}}}}

    def data(self,scope):
        return {'printer':'TEST','material':'PLA','grams':'50','duration_seconds':3600,
                'process_settings':{'bed_temp':'60','nozzle_temp':'220','duration_scope':scope}}

    def test_print_only_adds_preparation_once(self):
        result=estimate_energy(self.data('PRINT_ONLY'),self.policy())
        self.assertEqual(Decimal(result['kwh']),Decimal('.23'))
        self.assertEqual(result['pricing_print_seconds'],'3600')
        self.assertEqual(result['warmup_wh'],30)

    def test_total_duration_replaces_preparation_interval(self):
        result=estimate_energy(self.data('TOTAL_WITH_PREPARATION'),self.policy())
        self.assertAlmostEqual(float(result['kwh']),200*3000/3600000+.03)
        self.assertEqual(Decimal(result['pricing_print_seconds']),Decimal(3000))
        self.assertEqual(result['preparation_method'],'HA_MATCHED_PREPARATION_HISTORY')

    def test_unknown_scope_keeps_fallback_and_exposes_observation(self):
        policy=self.policy();result=estimate_energy(self.data('UNKNOWN'),policy)
        policy['energy_telemetry'].pop('preparation')
        baseline=estimate_energy(self.data('UNKNOWN'),policy)
        self.assertEqual(result['kwh'],baseline['kwh'])
        self.assertIsNotNone(result['preparation_reference'])
        self.assertIn('PREPARATION_DURATION_SCOPE_UNKNOWN_THEORETICAL_WARMUP',result['assumptions'])

    def test_mismatched_temperature_and_stale_session_are_not_calibration(self):
        for change in ({'bed_c':100},{'nozzle_c':280},{'end_ts':-3000000}):
            with self.subTest(change=change):
                policy=self.policy()
                policy['energy_telemetry']['preparation']['TEST']['sessions'][0].update(change)
                result=estimate_energy(self.data('PRINT_ONLY'),policy)
                self.assertIsNone(result['preparation_reference'])
                self.assertEqual(result['preparation_method'],'THEORETICAL_COLD_START')

    def test_preparation_longer_than_total_and_zero_duration(self):
        data=self.data('TOTAL_WITH_PREPARATION');data['duration_seconds']=120
        result=estimate_energy(data,self.policy())
        self.assertIn('PREPARATION_LONGER_THAN_TOTAL_DURATION_FALLBACK',result['assumptions'])
        data['duration_seconds']=0
        self.assertEqual(Decimal(estimate_energy(data,self.policy())['kwh']),0)

    def test_thermal_fallback_does_not_claim_dryer_power(self):
        policy=self.policy();policy['energy_telemetry']['profiles']={}
        result=estimate_energy(self.data('UNKNOWN'),policy)
        self.assertEqual(result['accessory_energy_accounting'],'NOT_CALIBRATED')
        self.assertIn('ATTACHED_ACCESSORY_POWER_NOT_CALIBRATED',result['assumptions'])


if __name__=='__main__':unittest.main()
