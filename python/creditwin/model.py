from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class Parameters:
    heater_capacity_j_k: float = 120.0
    shell_capacity_j_k: float = 900.0
    heater_shell_conductance_w_k: float = 2.8
    shell_ambient_conductance_w_k: float = 0.75
    sensor_tau_s: float = 4.0
    ambient_k: float = 293.15

class ThermalModel:
    """Two thermal masses plus a first-order temperature sensor."""
    def __init__(self, p: Parameters = Parameters()):
        if min(p.heater_capacity_j_k, p.shell_capacity_j_k, p.sensor_tau_s) <= 0:
            raise ValueError("capacities and sensor time constant must be positive")
        if min(p.heater_shell_conductance_w_k, p.shell_ambient_conductance_w_k) < 0:
            raise ValueError("conductances cannot be negative")
        self.p = p

    def derivative(self, x, power_w):
        th, ts, tm = np.asarray(x, dtype=float)
        q_hs = self.p.heater_shell_conductance_w_k * (th - ts)
        q_sa = self.p.shell_ambient_conductance_w_k * (ts - self.p.ambient_k)
        return np.array([(power_w-q_hs)/self.p.heater_capacity_j_k,
                         (q_hs-q_sa)/self.p.shell_capacity_j_k,
                         (ts-tm)/self.p.sensor_tau_s])

    def step(self, x, power_w, dt_s):
        if dt_s <= 0: raise ValueError("dt_s must be positive")
        x=np.asarray(x,dtype=float); f=self.derivative
        k1=f(x,power_w); k2=f(x+0.5*dt_s*k1,power_w)
        k3=f(x+0.5*dt_s*k2,power_w); k4=f(x+dt_s*k3,power_w)
        return x + dt_s*(k1+2*k2+2*k3+k4)/6

    def simulate(self, duration_s=1200.0, dt_s=0.5, power_w=40.0, initial_k=None):
        x=np.array(initial_k if initial_k is not None else [self.p.ambient_k]*3,dtype=float)
        times=np.arange(0.0,duration_s+0.5*dt_s,dt_s)
        states=np.empty((len(times),3)); states[0]=x
        residual=np.zeros(len(times)); e_in=e_loss=0.; x0=x.copy()
        for i in range(1,len(times)):
            loss0=self.p.shell_ambient_conductance_w_k*(x[1]-self.p.ambient_k)
            xn=self.step(x,power_w,dt_s)
            loss1=self.p.shell_ambient_conductance_w_k*(xn[1]-self.p.ambient_k)
            e_in += power_w*dt_s; e_loss += 0.5*(loss0+loss1)*dt_s
            x=xn; states[i]=x
            stored=self.p.heater_capacity_j_k*(x[0]-x0[0])+self.p.shell_capacity_j_k*(x[1]-x0[1])
            residual[i]=e_in-e_loss-stored
        return times, states, residual
