# Functionality to open files
import os
# Stats library
import numpy as np
# For debugging purposes
import pdb
# Math library
import math as m

# This function parses scans (one rotation recording by the lidar)
def parse_scan(line):
    result = []
    row = line.split(';')
    for item in row:
        result.append(float(item.split('|')[0]))
    return result

def find_first_middle_value(xy_values, timestamps):
    u = 0
    for row in xy_values:
        for item in row:
            if item[0] == 0:
                return (timestamps[u], item)
        u+=1

# Open UBH file
with open('file.ubh') as recording:
    end_result = []
    timestamps = []
    ps = False
    pt = False

    i = 0
    # Iterate all records in the recording
    for line in recording:
        result = []
        if line.strip() == '[timestamp]':
            pt = True
        # This signifies the next line will be a scan
        elif line.strip() == '[scan]':
            ps = True
        elif pt == True:
            pt = False
            timestamps.append(line.strip())
        elif ps == True:
            ps = False
            # All scans are appended to the end_result for further processing
            end_result.append(parse_scan(line))
            i+=1

    # Turn end result into a 2D matrix with i rows (amount of scans)
    # and 1081 cols (amount of snapshots in a scan)
    lidar_distances = np.array(end_result).reshape((i,1081))
    xy_values = []
    k = 0

    # Iterate over every row (scan)
    for item in lidar_distances:
        j = 0
        row = []
        # Iterate over every item in row (snapshot)
        for thing in item:
            # 60000(mm) is the max distance the lidar measures
            # If the distance is less than 60000 it means the lidar measured something
            if thing != 60000:
                # The lidar measures an area with radius of 60000mm and 270deg.
                # Each lidar measurement is converted to an x and y value by multiplying the distance 
                # with the cos and sin of the angle.
                # The x and y axis intersect at the camera itself
                # To get the angle of a snapshot, multiply the iteration by 0.25deg (the angle in deg of each snapshot)
                
                # Positive x value
                if j < 540:
                    value = (thing*m.cos(m.radians(j*0.25-45)), thing*m.sin(m.radians(j*0.25-45)))
                # The y axis
                elif j == 540:
                    value = (0,thing)
                # Negative x value
                else:
                    value = (-thing*m.cos(m.radians(225-j*0.25)), thing*m.sin(m.radians(225-j*0.25)))
                row.append(value)
            j+=1
        xy_values.append(row)
        k+=1

    first_row = xy_values[0]
    last_row = xy_values[len(xy_values) - 1]

    first_value = first_row[len(first_row) - 1]
    last_value = last_row[0]

    first_timestamp = timestamps[0]
    last_timestamp = timestamps[len(xy_values) - 1]

    middle = find_first_middle_value(xy_values, timestamps)
    middle_timestamp = middle[0]
    middle_value = middle[1]


    print('First')
    print(first_timestamp)
    print(first_value)
    #print(last_timestamp)
    #print(last_value)
    print('Middle')
    print(middle_timestamp)
    print(middle_value)

    print('Diff')
    print(int(middle_timestamp) - int(first_timestamp))
    print(first_value[0])

    

    
