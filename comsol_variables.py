# -*- coding: utf-8 -*-
"""
Created on Fri May  3 15:40:29 2024

@author: dsotnikov87
"""

import pandas as pd
import numpy as np
import os
import re

#%% Create set of parameters by imported .csv files from COMSOL

# Determine the folder where placed all exported files
path = str(r'C:\Users\sotnik_d\Desktop\Work\60_Collaboration\06_Quanscient\01_gmsh for 16T').replace('/', r'\/')

files = os.listdir(path)

# Create dictionary with all variables
list_of_variables = {}

for i in files:
    
    # Select only files of .csv type
    if '.csv' in i:
        
        data = pd.read_csv(path+'\\'+i, header = None)
        
        var_names = list(data[0])               # list of parameters and variables names
        var_value = list(map(str, data[1]))     # list of parameters and variables values, in string type
        
        # Loop for each parameter or variable format determining
        for j in range(len(var_names)):
            
            # Selection of parameter in scientific format
            value = re.findall(r"[-+]?\d*+e[-+]?\d+", var_value[j])
            if value != list([]):
                value = float(value[0])   
                print('Scientific format: ', var_value[j], value)
            
            # Selection of parameter in double format
            if value == list([]):
                value = re.findall(r'[-+]?\b\d+\.\d+\b', var_value[j])
                if value != list([]):
                    value = float(value[0])
                    print('Double format: ', var_value[j], value)
            
            # Selection of integer parameter
            if value == list([]):
                value = re.findall(r'[-+]?\d+', var_value[j])
                if value != list([]):
                    value = int(value[0]) 
                    print('Integer format: ', var_value[j], value)
            
            # If no one format from above, take string format
            if value == list([]):
                value = var_value[j]
                print('String format: ', var_value[j], value)
            
            # Declare parameter as python variable, taken from 
            # https://www.pythonforbeginners.com/basics/convert-string-to-variable-name-in-python
            myStr = var_names[j]
            myVal = value
            list_of_variables[myStr] = myVal
            myTemplate = "{} = \"{}\""
            statement = myTemplate.format(myStr, myVal)
            exec(statement)
            
#%% Real values of variables

# Convert to float format for numeric parameters
for i in list_of_variables:
    
    if list_of_variables[i] != str(list_of_variables[i]):
        
        globals()[i] = float(list_of_variables[i])


for i in list_of_variables:
    
    if list_of_variables[i] == str(list_of_variables[i]):
        
        # Select the case of parameters multiplication
        if '*' in list_of_variables[i]:
            
            variable_split = list_of_variables[i].split('*')
            variable_sum = 1
            for j in range(int(np.ceil(len(variable_split)/2))):
                
                variable_sum = variable_sum * float(globals()[variable_split[j*2]])
        
        # If no multiplication, then choose summation of parameters
        else:
            variable_split = list_of_variables[i].split()
            variable_sum = 0
            for j in range(int(np.ceil(len(variable_split)/2))):
                
                variable_sum += float(globals()[variable_split[j*2]])
        
        globals()[i] = variable_sum
        
#%% Display all results

for i in list_of_variables:
    
    print(i, ' = ', globals()[i])