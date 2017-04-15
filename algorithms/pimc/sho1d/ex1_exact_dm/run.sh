#!/bin/bash

nsample=400
nequil=100

echo "# omega beta sigma  accept  corr(x2)  x2  dx2" > x2_omega.dat
for omega in 2.0 5.0 10.0 20.0 25.0
do
  ./exact_dm.py -n $nsample -o $omega -opt -neq $nequil >> x2_omega.dat
done
