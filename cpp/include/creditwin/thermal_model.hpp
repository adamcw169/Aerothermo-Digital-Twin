#pragma once
#include <vector>
namespace creditwin {
struct Parameters {
  double heater_capacity_j_k{120.0};
  double shell_capacity_j_k{900.0};
  double heater_shell_conductance_w_k{2.8};
  double shell_ambient_conductance_w_k{0.75};
  double sensor_tau_s{4.0};
  double ambient_k{293.15};
};
struct State { double heater_k; double shell_k; double sensor_k; };
struct Sample { double time_s; State state; double energy_residual_j; };
class ThermalModel {
 public:
  explicit ThermalModel(Parameters parameters);
  State derivative(const State& state, double power_w) const;
  State rk4_step(const State& state, double power_w, double dt_s) const;
  std::vector<Sample> simulate(State initial, double power_w, double duration_s, double dt_s) const;
 private:
  Parameters p_;
};
}
