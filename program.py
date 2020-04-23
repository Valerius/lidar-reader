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

def last(list):
    return list[-1]

def first(list):
    return list[0]

def trace_beginning_of_train(xy_values, timestamps):
    result = []
    u = 0
    for row in xy_values:
        # Front of the train
        last_item = last(row)
        # If front of train has passed the y-axis, then stop
        if last_item[0] <= 0:
            return result
        # The front of the train is a bit further from the lidar
        elif last_item[1] > 3000:
            result.append((timestamps[u], last_item))
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

    # Collection of points of the front of the train until it reaches the y-axis
    train_front_trace = trace_beginning_of_train(xy_values, timestamps)
    # Approximately the moment the train hits the y-axis
    last_front_trace = last(train_front_trace)
    # Time in milliseconds the train needs to reach the y-axis
    total_time_interval = int(last_front_trace[0]) - int(train_front_trace[0][0])
    print(total_time_interval)
    speeds = []

    # Calculate the speed of the train at each given snapshot
    for item in train_front_trace:
        # millimeters
        distance = item[1][0] - last_front_trace[1][0]
        # milliseconds
        time_interval = int(last_front_trace[0]) - int(item[0])
        if time_interval != 0:
            # Speed in m/s
            speed = distance/time_interval
            speeds.append((speed, time_interval))

    average_accelleration = (last(speeds)[0] - speeds[0][0]) / (total_time_interval / 1000)
    print(average_accelleration)

