# -*- coding: utf-8 -*-
"""
Monte Carlo Error Propagation Example 1
    This code takes some data with Gaussian uncertainties and propagates them
    through a function.

    Both output means with standard deviation uncertainties and medians with
        with 68.3% coverage uncertainties are estimated.
    If the mean and standard deviation and median ; if the two methods give
        inconsistent results, then the output results do not have Gaussian
        uncertainties.

    Copyright (c) 2017 University of Toronto
    Original Version:   19 February 2017 by David Bailey
    Contact: David Bailey <dbailey@physics.utoronto.ca>
                (www.physics.utoronto.ca/~dbailey)
    License: Released under the MIT License; the full terms are appended
                to the end of this file, and are also available
                at www.opensource.org/licenses/mit-license.php
"""
from __future__ import print_function # Make print Python 2 or 3 compatible
from numpy import mean, std   # mean and standard deviation functions
from random import gauss      # random gaussian distribution

# Define function that takes measured data and outputs calculated result;
#   this is the function we want to propagate the uncertainties through.
#   The inputs to this function are only the values, not their uncertainties.
def func(data) :
    # Replace this function with your own!
    return data[0]+data[2]/data[1]

# Measured input data (values, uncertainties)
#   This example has non-Gaussian output uncertainties; if the uncertainties
#   were ten times smaller, the outputs would be Gaussian. Try it and see!
k_0  = (0.60, 0.04)
k_1  = (0.04, 0.01)
k_2  = (0.30, 0.02)
# Load input values into data list for input to function
data = (k_0,k_1,k_2)

# Number of Monte Carlo measurements to generate
#   This should be large enough to give reasonable accuracy in its output
#   without taking too much time.
N_MC = 3001 # Odd number makes median unbiased.

output_MC = []
data_MC = len(data)*[None]
# Monte Carlo loop generates an output for random input data distributed
#   according the the measured data values and uncertainties.
for i in range(N_MC) :
    # Generate random values for each input variable from a Gaussian
    #    distribution centered on the measured value and with standard
    #    deviation equalto the evaluated uncertainty
    for j in range(len(data)):
        data_MC[j] = gauss(*data[j])
    # Calculate Monte Carlo output values
    output_MC.append(func(data_MC))

# Print mean and standard deviation of Monte Carlo values
print("y_mean     =",mean(output_MC),"±", std(output_MC))

# Sort Monte Carlo values so that median and percentiles can be determined
output_MC = sorted(output_MC)

# Indices of -1 sigma,  Median, +1 sigma points of distribution
i_16     = int(N_MC*0.158655254)
i_median = int(N_MC*0.5)
i_84     = int(N_MC*0.841344746)

# Print median and 68.3% interval uncertainties
print("y_median   =", output_MC[i_median],
                        "+", output_MC[i_84]-output_MC[i_median],
                        "-", output_MC[i_median]-output_MC[i_16])


## Display distribution of output values
from matplotlib import pyplot

# Histogram output data
from numpy import histogram, multiply
# Use 1 to 99% percentile interval to define histogram range
i_1, i_99 = int(N_MC*0.01), int(N_MC*0.99) 
h,bin_edges = histogram(output_MC,bins=41,
                        range=(output_MC[i_1],output_MC[i_99]))

# Plot histogram
x = []
bin_width = bin_edges[1]-bin_edges[0]
scale_MC = 1./(bin_width*N_MC)
for i in range(len(bin_edges)-1) :
    x.append((bin_edges[i+1]+bin_edges[i])/2.)
pyplot.clf()
pyplot.yscale('log')
pyplot.bar(bin_edges[:-1],multiply(scale_MC,h),width=bin_width,color='pink')

# Plot Gaussian distribution for comparison
def gaussian(x, mu, sigma):
    # Returns the probability for observing a value x from a Gaussian 
    #   distribution with mean mu and standard deviation sigma.
    #   Works for either single values or lists of x.
    from math import exp,pi,sqrt
    if isinstance(x,list) :
        y=[]
        K = 1./(sqrt(2*pi)*sigma)
        S = 1./(2*sigma**2)
        for i in range(len(x)) :
            y.append(K*exp(-S*(x[i] - mu)**2))
        return y
    else :
        return exp(-(x - mu)**2/(2*sigma**2))/(sqrt(2*pi)*sigma)
pyplot.errorbar(x,gaussian(x,mean(output_MC),std(output_MC)), color="green")

pyplot.show()

"""
Full text of MIT License:

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
