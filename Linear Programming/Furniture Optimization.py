#!/usr/bin/env python
# coding: utf-8

from IPython.display import Image
Image(filename = r"Veerman Example.PNG", width=875)


import pandas as pd
from pulp import *


# initialize problem
prob = LpProblem("Title",LpMaximize)


# Create Variables
C = LpVariable("Chair",0)


# Objective Function

# Objective Function
prob += , "Total Profit"


# Constraints
# Constraints

#Fabrication Constraint
prob += , "Fabrication Constraint"

# Assembly Constraint


# Shipping Constraint


# Demand Constraints


# Maximization so C >= 0, D >=0, T >= 0 is implicit


# Solve and Status

prob.solve()
print("Status:", LpStatus[prob.status])


# Objective Solve

print("Total Profit = ", value(prob.objective))


# Optimal Values

# Each of the variables is printed with it's resolved optimum value
for v in prob.variables():
    print(v.name, "=", v.varValue)


# Shadow Prices and Slack

o = [{'name':name, 'shadow price':c.pi, 'slack': c.slack} 
     for name, c in prob.constraints.items()]
print(pd.DataFrame(o))


# Complete LP Problem Setup

print(prob)


# What Constraints are binding? <br>

# Increase fabrication to 1851, what happens to the objecctive value? <br>
# 

# Is Assembly a binding constraint? <br>
# Increase Assembly to 2401, what happens to the objective value?

# So if we have a new product "Stool" and it takes: <br>
#     - 3 hours fabrication <br>
#     - 2 hours assembly <br>
#     - 2 hours shipping <br>
# Is it profitable to make this new product? <br>

# Profit - Hours_Fabrication x Shadow_Price - Hours_Assembly x Shadow_Price - Hours_Shipping x Shadow_Price <br>
# 10 - 3 x (4) - 2 x (0) - 2 x (0) = -2 <br>
# <br>
# This is good for small changes, if other factors change, rerunning the problem is better <br>
