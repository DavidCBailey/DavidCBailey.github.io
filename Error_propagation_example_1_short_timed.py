# -*- coding: utf-8 -*-
from __future__ import print_function
from numpy import mean, std
from random import gauss
from time import time

start_time = time()

def func(data) :
    return data[0]+data[2]/data[1]

k_0  = (0.60, 0.04)
k_1  = (0.03, 0.01)
k_2  = (0.30, 0.02)
data = (k_0,k_1,k_2)

N_MC = 1000001
output_MC = []
data_MC = len(data)*[None]
for i in range(N_MC) :
    for j in range(len(data)):
        data_MC[j] = gauss(*data[j])
    output_MC.append(func(data_MC))

print("y_mean     =",mean(output_MC),"±", std(output_MC))

output_MC = sorted(output_MC)
i_16     = int(N_MC*0.158655254)
i_median = int(N_MC*0.5)
i_84     = int(N_MC*0.841344746)

print("y_median   =", output_MC[i_median],
                        "+", output_MC[i_84]-output_MC[i_median],
                        "-", output_MC[i_median]-output_MC[i_16])

end_time = time()
print("Time taken : ",end_time-start_time,"s")
