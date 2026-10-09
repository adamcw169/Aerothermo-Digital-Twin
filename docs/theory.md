# Model theory

The reduced model contains heater and shell thermal masses plus a first-order sensor. For thermal node i:

`C_i dT_i/dt = sum_j G_ij(T_j - T_i) + Q_i - Q_loss,i`

External loss is linearised as `G_sa(T_shell - T_ambient)`. This is intentionally lower fidelity than separate convection and radiation models. The simplification makes the model interpretable and computationally inexpensive, but limits extrapolation.

The sensor obeys `tau_s dT_sensor/dt = T_shell - T_sensor`. Time integration uses classical fourth-order Runge-Kutta. Energy accounting is evaluated independently from the state equations using trapezoidal integration of ambient heat loss.
