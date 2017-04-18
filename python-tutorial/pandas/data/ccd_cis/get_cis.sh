#!/bin/bash

template=./sep1.40-cis.inp
fname=sep1.40-cis.inp

#for sep in 0.80 0.90; do
for first in 1 2; do
  for second in {0..9}; do
    sep=${first}.${second}0
    subdir=sep$sep
    prefix=sep${sep}-cis
    mkdir $subdir
    cp $template $subdir
    cd $subdir
      mv $fname $prefix.inp
      sed -i "s/1.40000000/${sep}0000000/" $prefix.inp
      rungms $prefix.inp > $prefix.out
    cd ..
  done
done
