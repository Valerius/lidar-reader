import os
import numpy as np
import pdb
import math as m

def parse_scan(line):
    result = []
    row = line.split(';')
    for item in row:
        result.append(float(item.split('|')[0]))
    return result


with open('file.ubh') as recording:
    end_result = []
    ps = False

    running = True

    i = 0
    for line in recording:
        result = []
        if line.strip() == '[scan]':
            ps = True
        elif ps == True:
            ps = False
            end_result.append(parse_scan(line))
            i+=1

    lidar_distances = np.array(end_result).reshape((i,1081))
    k = 0
    for item in lidar_distances:
        j = 0
        for thing in item:
            if thing != 60000:
                if j < 540:
                    value = (thing*m.sin(j*0.25-45), thing*m.cos(j*0.25-45))
                elif j == 540:
                    value = (0,thing)
                else:
                    value = (thing*m.sin(j*0.25-225), -thing*m.cos(j*0.25-225))
            j+=1
        k+=1

    
