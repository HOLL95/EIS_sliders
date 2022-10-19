import os
import sys
dir=os.getcwd()
sys.path.append("src/")
from EIS_class import EIS
from pandas import read_csv
import numpy as np
import matplotlib.pyplot as plt
from circuit_drawer import circuit_artist
from Fit_explorer import explore_fit
data_loc="Data" #Folder where data is stored

file="EIS_WT_0.005V.csv" #File name
truncate_amount=35 #Amount of data to lop off the end
#File reading code
read_data=read_csv(data_loc+"/"+file, sep=",", encoding="unicode_escape", engine="python", skiprows=5, skipfooter=1)
numpy_data=read_data.to_numpy(copy=True, dtype='float')
freq=np.flip(numpy_data[:-truncate_amount,0])
real=(numpy_data[:-truncate_amount, 6])
imag=-(numpy_data[:-truncate_amount,7])
spectrum=np.column_stack((real, imag))


#Circuit structure -
#               Top level org: individual z-elements (in string z0, z1, z2 etc)
#               Normal elements defined as "zx":"param_name"
#               Paralell elements are defined as {"p1":"param_name1", "p2":"param_name2"}
#               Series elements in a paralell circuit are defined as a list - {"p1":"param_name1", "p2":["param_name2", "param_name3"]}
#               Resistor - "RX"
#               Capacitor - "CX"
#               Constant phase element - takes two params, so it's in a bracket ("QX", "alphaX")
circuit={
        'z1': {'p1': 'C1', 'p2': 'R1'}, 
        'z2': {'p1': ('Q1', 'alpha1'), 'p2': ('Q2', 'alpha2')}, 
        'z0': 'R0'}
#Parameters - needs to be in format {"Parameter_name(in speech marks)":Parameter_value (number)} <- all in curly braces
#Every parameter defined in the circuit needs to be given a value here!

parameter_dict={
                'R0': 8.243774205993775, 
                'C1': 3.0458203284686053e-05, 
                'R1': 545.6487404966642, 
                'Q1': 5.057273297064228e-06, 
                'alpha1': 0.6709512505395399, 
                'Q2': 0.005451035630044377, 
                'alpha2': 6.687463857129168e-17}
translator=EIS()
explore_fit(
        circuit, 
        parameter_dict, 
        frequencies=freq, #Defined frequencies
        data=spectrum, #If you want to plot data as well, otherwise delete
        bounds_factor=15, #The range of the slider - defined as [1/(bounds_factor)*parameter_dict_value, bounds_factor*parameter_dict_value]
        )
