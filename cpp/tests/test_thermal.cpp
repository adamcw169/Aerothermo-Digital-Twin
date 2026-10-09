#include "creditwin/thermal_model.hpp"
#include <cassert>
#include <cmath>
#include <iostream>
int main(){
  creditwin::ThermalModel model({});
  auto eq=model.simulate({293.15,293.15,293.15},0.0,100.0,0.5);
  assert(std::abs(eq.back().state.shell_k-293.15)<1e-12);
  auto run=model.simulate({293.15,293.15,293.15},40.0,1200.0,0.5);
  assert(run.back().state.heater_k>run.back().state.shell_k);
  assert(run.back().state.shell_k>293.15);
  assert(std::abs(run.back().energy_residual_j)<0.02);
  std::cout<<"All C++ tests passed\n";
}
