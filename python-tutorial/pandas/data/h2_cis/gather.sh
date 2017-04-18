grep 'EXCITED STATE   1  ENERGY' */*.out  | awk '{print $6}' > first.dat
grep 'RHF REFERENCE ENERGY' */*.out | awk '{print $6}' > ground.dat
