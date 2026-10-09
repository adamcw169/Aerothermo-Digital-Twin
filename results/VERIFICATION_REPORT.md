# Verification report

Status: **development only**. All observations in this report are synthetic.

## Configuration
- Duration: 1200 s
- Integration step: 0.5 s
- Constant electrical input: 40 W
- Integrator: fixed-step RK4

## Results
- Maximum absolute energy-balance residual: **0.000603 J**
- Zero-input equilibrium error: **0.000e+00 K**
- Calibrated synthetic-sensor RMSE: **0.1565 K**
- Estimated heater-shell conductance: **2.850 W/K**
- Estimated shell-ambient conductance: **0.825 W/K**
- Estimated sensor bias: **0.191 K**
- Monte Carlo final sensor-temperature 90% interval: **322.08–325.78 K**

## Interpretation
The checks verify internal implementation behaviour for the stated synthetic configuration. They do **not** experimentally validate the model or establish suitability for a real engineering decision.
