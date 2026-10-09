import json, platform, subprocess
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from .model import Parameters, ThermalModel
from .analytics import synthetic_observations, grid_calibrate, monte_carlo

def generate(root: Path):
    out=root/'results'; data=root/'data'/'synthetic'; out.mkdir(exist_ok=True); data.mkdir(parents=True,exist_ok=True)
    truth_p=Parameters(heater_shell_conductance_w_k=3.05,shell_ambient_conductance_w_k=.82)
    t,s,res=ThermalModel(truth_p).simulate(); obs=synthetic_observations(t,s[:,2])
    np.savetxt(data/'synthetic_nominal.csv',np.c_[t,s,obs],delimiter=',',header='time_s,heater_k,shell_k,sensor_truth_k,sensor_observed_k',comments='')
    rmse,fit,bias=grid_calibrate(t,obs); _,sf,_=ThermalModel(fit).simulate(); mc=monte_carlo()
    metrics={
      'schema_version':'0.1.0','status':'development_only','synthetic_data':True,
      'simulation':{'duration_s':1200.0,'dt_s':0.5,'power_w':40.0,'samples':len(t)},
      'verification':{'max_abs_energy_residual_j':float(np.max(np.abs(res))),
        'equilibrium_error_k':float(abs(ThermalModel().simulate(100,0.5,0)[1][-1,1]-293.15))},
      'calibration':{'method':'bounded grid search','sensor_rmse_k':rmse,
        'estimated_heater_shell_conductance_w_k':fit.heater_shell_conductance_w_k,
        'estimated_shell_ambient_conductance_w_k':fit.shell_ambient_conductance_w_k,'estimated_sensor_bias_k':bias},
      'uncertainty':{'method':'Monte Carlo','samples':len(mc),'final_sensor_k_p05':float(np.quantile(mc,.05)),
        'final_sensor_k_median':float(np.median(mc)),'final_sensor_k_p95':float(np.quantile(mc,.95))},
      'environment':{'python':platform.python_version(),'platform':platform.platform()}}
    (out/'verification_report.json').write_text(json.dumps(metrics,indent=2)+'\n')
    fig,ax=plt.subplots(figsize=(9,5)); ax.plot(t,s[:,0]-273.15,label='Heater truth'); ax.plot(t,s[:,1]-273.15,label='Shell truth');
    ax.scatter(t[::40],obs[::40]-273.15,s=8,label='Synthetic measurements'); ax.plot(t,sf[:,2]+bias-273.15,'--',label='Calibrated sensor model')
    ax.set(xlabel='Time [s]',ylabel='Temperature [°C]',title='Synthetic thermal experiment and calibrated model'); ax.grid(True,alpha=.25); ax.legend(); fig.tight_layout(); fig.savefig(out/'nominal_calibration.png',dpi=180); plt.close(fig)
    md=f"""# Verification report\n\nStatus: **development only**. All observations in this report are synthetic.\n\n## Configuration\n- Duration: 1200 s\n- Integration step: 0.5 s\n- Constant electrical input: 40 W\n- Integrator: fixed-step RK4\n\n## Results\n- Maximum absolute energy-balance residual: **{metrics['verification']['max_abs_energy_residual_j']:.6f} J**\n- Zero-input equilibrium error: **{metrics['verification']['equilibrium_error_k']:.3e} K**\n- Calibrated synthetic-sensor RMSE: **{rmse:.4f} K**\n- Estimated heater-shell conductance: **{fit.heater_shell_conductance_w_k:.3f} W/K**\n- Estimated shell-ambient conductance: **{fit.shell_ambient_conductance_w_k:.3f} W/K**
- Estimated sensor bias: **{bias:.3f} K**\n- Monte Carlo final sensor-temperature 90% interval: **{metrics['uncertainty']['final_sensor_k_p05']:.2f}–{metrics['uncertainty']['final_sensor_k_p95']:.2f} K**\n\n## Interpretation\nThe checks verify internal implementation behaviour for the stated synthetic configuration. They do **not** experimentally validate the model or establish suitability for a real engineering decision.\n"""
    (out/'VERIFICATION_REPORT.md').write_text(md)
    return metrics
