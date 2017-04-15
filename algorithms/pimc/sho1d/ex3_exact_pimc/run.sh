#!/bin/bash

nsample=400

echo "# omega beta sigma  accept  corr(x2)  x2  dx2" > x2_omega.dat
for omega in 5.0 10.0 20.0 25.0
do
  ./pimc1d.py -n $nsample -o $omega --nequil 10 -opt >> x2_omega.dat
done
