#!/bin/bash

nsample=400
nslice=20

echo "# omega beta sigma  accept  corr(x2)  x2  dx2" > x2_omega.dat
for omega in 5.0 10.0 20.0 25.0
do
  ../main.py -n $nsample -ns $nslice -o $omega --nequil 50 >> x2_omega.dat
done
