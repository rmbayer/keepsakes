#!/usr/bin/env python
# coding: utf-8

from IPython.display import Image
Image(filename = r"Car Problem.PNG", width=875)


# ### Ignore the Fuel Economy Constraint!

import pandas as pd
from pulp import *


# initialize problem
prob = LpProblem("",)

# Initialize empty variables for how many cars to make
x = LpVariable("",0)


# Objective Function

prob += _____, ""


# Constraints

prob +=  +  +  +  <= , " Constraint"

# Capacity Constraints
prob += 

# Market Demand Potential
prob += 

# Fuel Constraints
# IGNORE

# Subcompact and Compacts Constraint
prob += 


# Solve and Status

# No Need to Edit
prob.solve()
print("Status:", LpStatus[prob.status])


# Objective Solve

print("____ = ", value(prob.objective))


# Optimal Values

# No Need to Edit
# Each of the variables is printed with it's resolved optimum value
for v in prob.variables():
    print(v.name, "=", v.varValue)


# Shadow Prices and Slack

# No Need to Edit
o = [{'name':name, 'shadow price':c.pi, 'slack': c.slack} 
     for name, c in prob.constraints.items()]
print(pd.DataFrame(o))


# Complete LP Problem Setup
print(prob)

