#include "creditwin/thermal_model.hpp"
#include <fstream>
#include <iomanip>
#include <iostream>
int main(int argc,char**argv){
  const std::string path=argc>1?argv[1]:"cpp_results.csv";
  creditwin::ThermalModel model({});
  auto samples=model.simulate({293.15,293.15,293.15},40.0,1200.0,0.5);
  std::ofstream f(path); f<<"time_s,heater_k,shell_k,sensor_k,energy_residual_j\n"<<std::setprecision(12);
  for(const auto& x:samples) f<<x.time_s<<','<<x.state.heater_k<<','<<x.state.shell_k<<','<<x.state.sensor_k<<','<<x.energy_residual_j<<'\n';
  std::cout<<"Wrote "<<samples.size()<<" samples to "<<path<<"\n";
}
