from pulp import *

# Create the 'prob' variable to contain the problem data
prob = LpProblem("The Whiskas Problem",LpMinimize)

# The 2 variables Beef and Chicken are created with a lower limit of zero
x1=LpVariable("ChickenPercent",0,None,LpInteger)
x2=LpVariable("BeefPercent",0)

# The objective function is added to 'prob' first
prob += 0.013*x1 + 0.008*x2, "Total Cost of Ingredients per can"

# The five constraints are entered
prob += x1 + x2 == 100, "PercentagesSum"
prob += 0.100*x1 + 0.200*x2 >= 8.0, "ProteinRequirement"
prob += 0.080*x1 + 0.100*x2 >= 6.0, "FatRequirement"
prob += 0.001*x1 + 0.005*x2 <= 2.0, "FibreRequirement"
prob += 0.002*x1 + 0.005*x2 <= 0.4, "SaltRequirement"

# The problem data is written to an .lp file
#prob.writeLP("WhiskasModel.lp")

# The problem is solved using PuLP's choice of Solver
prob.solve()

# The status of the solution is printed to the screen
print("Status:", LpStatus[prob.status])

# Each of the variables is printed with it's resolved optimum value
for v in prob.variables():
    print(v.name, "=", v.varValue)
    
# The optimised objective function value is printed to the screen
print("Total Cost of Ingredients per can = ", value(prob.objective))


###############################################################################
import pandas as pd
data = pd.read_csv(r"Whiskas LP.csv")
data = data.set_index('Stuff')

data.loc['Beef']['Cost']


prob = LpProblem("The Whiskas Problem",LpMinimize)

# The 2 variables Beef and Chicken are created with a lower limit of zero
x1=LpVariable("ChickenPercent",0,None,LpInteger)
x2=LpVariable("BeefPercent",0)

# Objective Function
prob += data.loc['Chicken']['Cost'] * x1 +  \
        data.loc['Beef']['Cost'] * x2, \
        "Total Cost of Ingredients per can"


# Constraints
prob += x1 + x2 == 100, "PercentagesSum"

prob += data.loc['Chicken']['Protein']  *x1 + \
        data.loc['Beef']['Protein']     *x2 >= 8.0, "ProteinRequirement"
        
prob += data.loc['Chicken']['Fat']      *x1 + \
        data.loc['Beef']['Fat']         *x2 >= 6.0, "FatRequirement"
        
prob += data.loc['Chicken']['Fibre']    *x1 + \
        data.loc['Beef']['Fibre']       *x2 <= 2.0, "FibreRequirement"
        
prob += data.loc['Chicken']['Salt']     *x1 +\
        data.loc['Beef']['Salt']        *x2 <= 0.4, "SaltRequirement"

# The problem data is written to an .lp file
#prob.writeLP("WhiskasModel.lp")

# The problem is solved using PuLP's choice of Solver
prob.solve()

# The status of the solution is printed to the screen
print("Status:", LpStatus[prob.status])

# Each of the variables is printed with it's resolved optimum value
for v in prob.variables():
    print(v.name, "=", v.varValue)
    
# The optimised objective function value is printed to the screen
print("Total Cost of Ingredients per can = ", value(prob.objective))

###############################################################################

# Creates a list of the Ingredients
Ingredients = ['CHICKEN', 'BEEF', 'MUTTON', 'RICE', 'WHEAT', 'GEL']

# A dictionary of the costs of each of the Ingredients is created
costs = {'CHICKEN': 0.013, 
         'BEEF': 0.008, 
         'MUTTON': 0.010, 
         'RICE': 0.002, 
         'WHEAT': 0.005, 
         'GEL': 0.001}

# A dictionary of the protein percent in each of the Ingredients is created
proteinPercent = {'CHICKEN': 0.100, 
                  'BEEF': 0.200, 
                  'MUTTON': 0.150, 
                  'RICE': 0.000, 
                  'WHEAT': 0.040, 
                  'GEL': 0.000}

# A dictionary of the fat percent in each of the Ingredients is created
fatPercent = {'CHICKEN': 0.080, 
              'BEEF': 0.100, 
              'MUTTON': 0.110, 
              'RICE': 0.010, 
              'WHEAT': 0.010, 
              'GEL': 0.000}

# A dictionary of the fibre percent in each of the Ingredients is created
fibrePercent = {'CHICKEN': 0.001, 
                'BEEF': 0.005, 
                'MUTTON': 0.003, 
                'RICE': 0.100, 
                'WHEAT': 0.150, 
                'GEL': 0.000}

# A dictionary of the salt percent in each of the Ingredients is created
saltPercent = {'CHICKEN': 0.002, 
               'BEEF': 0.005, 
               'MUTTON': 0.007, 
               'RICE': 0.002, 
               'WHEAT': 0.008, 
               'GEL': 0.000}

# Create the 'prob' variable to contain the problem data
prob = LpProblem("The Whiskas Problem", LpMinimize)

# A dictionary called 'ingredient_vars' is created to contain the referenced Variables
ingredient_vars = LpVariable.dicts("Ingr",Ingredients,0)

# The objective function is added to 'prob' first
prob += lpSum([costs[i]*ingredient_vars[i] for i in Ingredients]), "Total Cost of Ingredients per can"


c1 = lpSum([ingredient_vars[i] for i in Ingredients]) == 100, "PercentagesSum"
c2 = lpSum([proteinPercent[i] * ingredient_vars[i] for i in Ingredients]) >= 8.0, "ProteinRequirement"
c3 = lpSum([fatPercent[i] * ingredient_vars[i] for i in Ingredients]) >= 6.0, "FatRequirement"
c4 = lpSum([fibrePercent[i] * ingredient_vars[i] for i in Ingredients]) <= 2.0, "FibreRequirement"
c5 = lpSum([saltPercent[i] * ingredient_vars[i] for i in Ingredients]) <= 0.4, "SaltRequirement"

for con in [c1,c2,c3,c4,c5]:
    prob += con

c6_LHS = LpAffineExpression([(ingredient_vars['GEL'],1), (ingredient_vars['BEEF'],1)])

c6= LpConstraint(e=c6_LHS, sense=-1, name='GelBeefTotal', rhs=30)

c6_elastic = c6.makeElasticSubProblem(penalty = 100, proportionFreeBoundList = [.02,.02])

prob.extend(c6_elastic)

#prob.writeLP("WhiskasModel.lp")
prob.solve()

# The five constraints are added to 'prob'
# prob += lpSum([ingredient_vars[i] for i in Ingredients]) == 100, "PercentagesSum"
# prob += lpSum([proteinPercent[i] * ingredient_vars[i] for i in Ingredients]) >= 8.0, "ProteinRequirement"
# prob += lpSum([fatPercent[i] * ingredient_vars[i] for i in Ingredients]) >= 6.0, "FatRequirement"
# prob += lpSum([fibrePercent[i] * ingredient_vars[i] for i in Ingredients]) <= 2.0, "FibreRequirement"
# prob += lpSum([saltPercent[i] * ingredient_vars[i] for i in Ingredients]) <= 0.4, "SaltRequirement"

# The problem data is written to an .lp file
prob.writeLP("WhiskasModel2.lp")

# The problem is solved using PuLP's choice of Solver
prob.solve()

# The status of the solution is printed to the screen
print("Status:", LpStatus[prob.status])

# Each of the variables is printed with it's resolved optimum value
for v in prob.variables():
    print(v.name, "=", v.varValue)

# The optimised objective function value is printed to the screen    
print("Total Cost of Ingredients per can = ", value(prob.objective))

