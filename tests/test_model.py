import unittest, numpy as np
from creditwin.model import ThermalModel
class ModelTests(unittest.TestCase):
 def test_zero_input_equilibrium(self):
  _,s,_=ThermalModel().simulate(100,0.5,0); self.assertLess(abs(s[-1,1]-293.15),1e-12)
 def test_heating_order(self):
  _,s,_=ThermalModel().simulate(); self.assertGreater(s[-1,0],s[-1,1]); self.assertGreater(s[-1,1],293.15)
 def test_energy_residual(self):
  _,_,r=ThermalModel().simulate(); self.assertLess(np.max(np.abs(r)),0.02)
if __name__=='__main__': unittest.main()
