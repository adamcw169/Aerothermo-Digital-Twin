from dataclasses import asdict, replace
import numpy as np
from .model import Parameters, ThermalModel

def single_node_exact(t, initial_k, ambient_k, power_w, capacity_j_k, conductance_w_k):
    steady=ambient_k+power_w/conductance_w_k
    return steady+(initial_k-steady)*np.exp(-conductance_w_k*np.asarray(t)/capacity_j_k)

def synthetic_observations(times, sensor_k, noise_sd_k=0.15, bias_k=0.10, seed=20261009):
    rng=np.random.default_rng(seed)
    return sensor_k+bias_k+rng.normal(0,noise_sd_k,len(times))

def grid_calibrate(times, observed_k, base=Parameters(), power_w=40.0):
    conductances=np.linspace(2.1,3.5,29)
    losses=np.linspace(0.45,1.05,25)
    stride=max(1,int(round(2.0/(times[1]-times[0]))))
    best=None
    for g in conductances:
        for loss in losses:
            p=replace(base,heater_shell_conductance_w_k=float(g),shell_ambient_conductance_w_k=float(loss))
            _,s,_=ThermalModel(p).simulate(float(times[-1]),float(times[1]-times[0]),power_w)
            residual=observed_k[::stride]-s[::stride,2]
            bias=float(np.mean(residual))
            rmse=float(np.sqrt(np.mean((residual-bias)**2)))
            if best is None or rmse<best[0]: best=(rmse,p,bias)
    return best

def monte_carlo(duration_s=1200.0, dt_s=2.0, power_w=40.0, n=300, seed=7):
    rng=np.random.default_rng(seed); final=[]
    for _ in range(n):
        p=Parameters(heater_capacity_j_k=rng.normal(120,6),shell_capacity_j_k=rng.normal(900,36),
          heater_shell_conductance_w_k=rng.normal(2.8,.14),shell_ambient_conductance_w_k=rng.normal(.75,.06),
          sensor_tau_s=max(.2,rng.normal(4,.4)),ambient_k=rng.normal(293.15,.3))
        _,s,_=ThermalModel(p).simulate(duration_s,dt_s,power_w); final.append(s[-1,2])
    return np.asarray(final)
