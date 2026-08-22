import unittest
from thermal import rho,simulate,metrics
class Tests(unittest.TestCase):
    def test_density(self): self.assertGreater(rho(0),rho(50000))
    def test_heating_positive(self): self.assertGreater(metrics(simulate(1))["peak_heat_flux_proxy_w_m2"],0)
    def test_temperature_finite(self): self.assertGreater(simulate(1)[-1]["surface_temp_k"],0)
if __name__=="__main__": unittest.main()
