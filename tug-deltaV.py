#!/usr/bin/python3

from math import exp
import random

Isp_chemical_seconds = 320
Isp_xenon_seconds = 1800
little_g = 9.81
tankage_fraction = 0.1
spacecraft_mass = 2000

deltaV_geo = 5800
deltaV_disposal = 150

collection_mass = 35000

def analyse(fuel_up, fuel_down, disposal_fuel, recovery_fuel):
    tank_mass = (fuel_up + fuel_down + recovery_fuel + disposal_fuel) * tankage_fraction
    heavy_sc = spacecraft_mass + tank_mass + recovery_fuel + disposal_fuel
    mass_ratio_up = (heavy_sc + fuel_up + fuel_down) / (heavy_sc + fuel_down)
    mass_ratio_down = (heavy_sc + collection_mass + fuel_down) / (heavy_sc + collection_mass)
    mass_ratio_disposal = (spacecraft_mass + tank_mass + collection_mass + recovery_fuel + disposal_fuel) / (spacecraft_mass + tank_mass + collection_mass + recovery_fuel)
    mass_ratio_recovery = (spacecraft_mass + tank_mass + recovery_fuel) / (spacecraft_mass + tank_mass)

    target_mass_ratio_up = exp(deltaV_geo / (Isp_xenon_seconds*little_g))
    target_mass_ratio_down = exp(deltaV_geo / (Isp_xenon_seconds*little_g))
    target_mass_ratio_disposal = exp(deltaV_disposal / (Isp_chemical_seconds*little_g))
    target_mass_ratio_recovery = exp(deltaV_disposal / (Isp_chemical_seconds*little_g))

    values=[target_mass_ratio_up, mass_ratio_up, target_mass_ratio_down, mass_ratio_down, target_mass_ratio_recovery, mass_ratio_recovery, target_mass_ratio_disposal, mass_ratio_disposal]
    TLM=heavy_sc+fuel_up+fuel_down
    problem=[values[2*i+1]-values[2*i] for i in range(4)]
    return [problem,TLM]

start_pt=[2218,2130,257,211]
print(start_pt, analyse(start_pt[0],start_pt[1],start_pt[2],start_pt[3]))
bsf=99999

for shot in range(20000000):
    aa = random.uniform(0,20000)
    bb = random.uniform(0,20000)
    cc = random.uniform(0,3000)
    dd = random.uniform(0,3000)
    UG = analyse(aa,bb,cc,dd)
    if (min(UG[0])>0.01):
        if (UG[1]<bsf):
            print([aa,bb,cc,dd], UG, UG[1], aa+bb+cc+dd, bsf)
            bsf = UG[1]