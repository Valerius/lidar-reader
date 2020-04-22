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
    xy_values = []
    k = 0
    for item in lidar_distances:
        j = 0
        row = []
        for thing in item:
            if thing != 60000:
                if j < 540:
                    value = (thing*m.cos(m.radians(j*0.25-45)), thing*m.sin(m.radians(j*0.25-45)))
                elif j == 540:
                    value = (0,thing)
                else:
                    value = (-thing*m.cos(m.radians(225-j*0.25)), thing*m.sin(m.radians(225-j*0.25)))
                row.append(value)
            j+=1
        xy_values.append(row)
        k+=1

    
