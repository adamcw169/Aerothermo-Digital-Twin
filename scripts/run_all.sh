#!/usr/bin/env bash
set -euo pipefail
export PYTHONPATH="${PYTHONPATH:-}:python"
python -m unittest discover -s tests -v
if command -v cmake >/dev/null 2>&1; then
  cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
  cmake --build build --parallel
  ctest --test-dir build --output-on-failure
else
  g++ -std=c++17 -O2 -Wall -Wextra -Wpedantic -Icpp/include cpp/src/thermal_model.cpp cpp/tests/test_thermal.cpp -o /tmp/creditwin_cpp_tests
  /tmp/creditwin_cpp_tests
fi
python -m creditwin.cli verify --root .
