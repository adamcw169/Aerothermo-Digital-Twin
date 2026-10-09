#include "creditwin/thermal_model.hpp"
#include <cmath>
#include <stdexcept>
namespace creditwin {
ThermalModel::ThermalModel(Parameters p) : p_(p) {
  if (p_.heater_capacity_j_k <= 0 || p_.shell_capacity_j_k <= 0 || p_.sensor_tau_s <= 0 ||
      p_.heater_shell_conductance_w_k < 0 || p_.shell_ambient_conductance_w_k < 0)
    throw std::invalid_argument("non-physical thermal parameters");
}
State ThermalModel::derivative(const State& s, double q) const {
  const double q_hs = p_.heater_shell_conductance_w_k * (s.heater_k - s.shell_k);
  const double q_sa = p_.shell_ambient_conductance_w_k * (s.shell_k - p_.ambient_k);
  return {(q - q_hs) / p_.heater_capacity_j_k,
          (q_hs - q_sa) / p_.shell_capacity_j_k,
          (s.shell_k - s.sensor_k) / p_.sensor_tau_s};
}
State ThermalModel::rk4_step(const State& s, double q, double dt) const {
  if (dt <= 0) throw std::invalid_argument("dt must be positive");
  auto add=[](State a, State b, double k){return State{a.heater_k+k*b.heater_k,a.shell_k+k*b.shell_k,a.sensor_k+k*b.sensor_k};};
  State k1=derivative(s,q), k2=derivative(add(s,k1,dt/2),q), k3=derivative(add(s,k2,dt/2),q), k4=derivative(add(s,k3,dt),q);
  return {s.heater_k+dt*(k1.heater_k+2*k2.heater_k+2*k3.heater_k+k4.heater_k)/6,
          s.shell_k+dt*(k1.shell_k+2*k2.shell_k+2*k3.shell_k+k4.shell_k)/6,
          s.sensor_k+dt*(k1.sensor_k+2*k2.sensor_k+2*k3.sensor_k+k4.sensor_k)/6};
}
std::vector<Sample> ThermalModel::simulate(State s, double q, double duration, double dt) const {
  if (duration < 0 || dt <= 0) throw std::invalid_argument("invalid simulation time");
  std::vector<Sample> out; double t=0, e_in=0, e_loss=0;
  const State initial=s;
  out.push_back({t,s,0});
  while (t + 1e-12 < duration) {
    const double h=std::min(dt,duration-t);
    const double loss0=p_.shell_ambient_conductance_w_k*(s.shell_k-p_.ambient_k);
    State next=rk4_step(s,q,h);
    const double loss1=p_.shell_ambient_conductance_w_k*(next.shell_k-p_.ambient_k);
    e_in += q*h; e_loss += 0.5*(loss0+loss1)*h;
    t += h; s=next;
    const double stored=p_.heater_capacity_j_k*(s.heater_k-initial.heater_k)+p_.shell_capacity_j_k*(s.shell_k-initial.shell_k);
    out.push_back({t,s,e_in-e_loss-stored});
  }
  return out;
}
}
