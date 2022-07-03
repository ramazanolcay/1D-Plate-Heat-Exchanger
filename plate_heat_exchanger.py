# -*- coding: utf-8 -*-
"""
Created on 23 14:19:56 2021
@author: ramazanolcay
"""
from CoolProp.CoolProp import PropsSI #Thermodynamic library
import numpy as np
import matplotlib.pyplot as plt

C_to_K = 273.15 # Celsius to kelvin converter
T1= 37.8 + C_to_K # Hot inlet as celsius
T2 = 30.9 + C_to_K # Hot outlet as celsius
T_ave_hot = ((T1 + T2) / 2)
P_hot = 10*10000 # as Pa
V_flow_rate_hot = 10 / (3600) # as m3 per second

Cp_hot = (PropsSI("C", "P", P_hot, "T", T_ave_hot, "Water"), "J/kg/K")
Cp_hot_float = (Cp_hot[0]) / 1000
del Cp_hot

ro_hot = (PropsSI("D", "T", T_ave_hot, "P", P_hot, "INCOMP::MEG-15%"), "kg/m^3")
ro_hot_float = ro_hot[0]
del ro_hot

mass_flow_rate_hot = (ro_hot_float * V_flow_rate_hot)
Q_hot = mass_flow_rate_hot * Cp_hot_float * (T1 - T2)
T3 = 16 + C_to_K # Cold inlet as celsius
P_cold = 6*10000 # as Pa
V_flow_rate_cold = 6.72 / (60*60) # as m3 per second


ro_cold = PropsSI("D", "T", T3, "P", P_cold, "Water"), "kg/m^3"
ro_cold_float = ro_cold[0]
del ro_cold


Cp_cold = (PropsSI("C", "D", ro_cold_float, "P", P_cold, "Water"), "J/kg/K")
Cp_cold_float = (Cp_cold[0]) / 1000
del Cp_cold


mass_flow_rate_cold = ro_cold_float * V_flow_rate_cold
T4 = (Q_hot / (mass_flow_rate_cold * Cp_cold_float)) + T3
T_ave_cold = (T3 + T4) / 2


Cp_cold = (PropsSI("C", "P", P_cold, "T", T4, "Water"), "J/kg/K")
Cp_cold_float = (Cp_cold[0]) / 1000
del Cp_cold

ro_cold = PropsSI("D", "T", T4, "P", P_cold, "Water"), "kg/m^3"
ro_cold_float = ro_cold[0]
del ro_cold


mass_flow_rate_cold = ro_cold_float * V_flow_rate_cold
T4 = (Q_hot / (mass_flow_rate_cold * Cp_cold_float)) + T3
print(f"T4 Value is: {(T4-C_to_K):.2f}°C")
print(f"Q is equal to: {Q_hot:.2f} kW")
efficiency = ((T4-T3) / (T1 - T3)) * 100
# print(f"Temperature efficiency is: {efficiency:.2f}%")
ln = np.log
LMTD_value = (((T1-T3)- (T2-T4)) / ln((T1-T3) / (T2-T4)))
print(f"LMTD value is: {LMTD_value:.2f}°C")
g_hot = [(T1 - C_to_K), (T2 - C_to_K)]
g_cold = [(T4 - C_to_K),(T3 - C_to_K)]

#GRAPH
plt.plot(g_hot, color="red", linewidth=5.0, linestyle="-", label="Hot",
marker=(9), markersize=15)
plt.ylim(0, 60)
plt.plot(g_cold, color="blue", linewidth=5.0, linestyle="-", label="Cold",
marker=(8), markersize=15)
plt.tick_params(axis='y', which='both', labelleft=True, labelright=True)
plt.legend(loc='upper right', prop={'size':15})
plt.yticks([T1-C_to_K, T2-C_to_K, T3- C_to_K, T4- C_to_K])
plt.gca().axes.xaxis.set_ticklabels([])
plt.title('Plate Heat Exchanger')
plt.ylabel("T (°C)")
plt.xlabel("Zaman (dt)")
plt.grid(True)
plt.savefig("Plate_Heat_Exchanger.pdf")
plt.savefig("Plate_Heat_Exchanger.png")
plt.show()
plt.close()