# Functionality to open files
import os
import sys
# Stats library
import numpy as np
# For debugging purposes
import pdb
# Math library
import math as m
# Import plotting library
import matplotlib.pyplot as plt
import gc
from datetime import datetime
from PyQt5 import QtWidgets
import pyqtgraph as pg

# Parse a scan (one rotation recording by the lidar), extracting the distance (x)
def parse_scan(line):
    result = []
    row = line.split(';')
    for item in row:
        result.append(float(item.split('|')[0]))
    return result

# Calculate the angle of one distance measurement of a scan.
# Each index represents an increase of 0.25 deg from the start of the rotation (index 0)
# The angle is converted to radians.
def calculate_angle(index):
    return m.radians(135 - index * 0.25)

# Using the angle and the distance, the x coordinate is calculated
def calculate_x_coordinate(distance, angle):
    return distance * m.sin(angle)

# Using the angle and the distance, the y coordinate is calculated
def calculate_y_coordinate(distance, angle):
    return distance * m.cos(angle)

# Using the index and the distance, the x and y coordinates are calculated
def calculate_coordinate(distance, index):
    angle = calculate_angle(index)
    x_coordinate = calculate_x_coordinate(distance, angle)
    y_coordinate = calculate_y_coordinate(distance, angle)
    return (x_coordinate, y_coordinate)

# Iterating over every scan in a recording, the coordinates are calculated
def calculate_coordinates(distances):
    result = []
    # Iterate over every row (scan)
    for scan in distances:
        row = []
        # Iterate over every item in row (snapshot)
        for i, distance in enumerate(scan):
            # 60000(mm) is the max distance the lidar measures
            # If the distance is less than 60000 it means the lidar measured something
            if distance != 60000:
                # The lidar measures an area with radius of 60000mm and 270deg.
                # Each lidar measurement is converted to an x and y value by multiplying the distance 
                # with the cos and sin of the angle.
                # The x and y axis intersect at the camera itself
                # To get the angle of a snapshot, multiply the iteration by 0.25deg (the angle in deg of each snapshot                
                coordinate = calculate_coordinate(distance, i)
                row.append(coordinate)

        result.append(row)
    return result

# The ubh file is parsed for the timestamps, the scans and the endStep
def get_timestamps_and_scans(recording):
    records = []
    timestamps = []
    endstep = None
    index = 0

    ps = False
    pt = False
    pe = False

    # Iterate all records in the recording
    for record in recording:
        stripped = record.strip()
        if stripped == '[timestamp]':
            pt = True
        # This signifies the next line will be a scan
        elif stripped == '[scan]':
            ps = True
        elif stripped == '[endStep]':
            pe = True
        elif pt:
            pt = False
            timestamps.append(int(stripped))
        elif ps:
            ps = False
            # All scans are appended to the end_result for further processing
            records.append(parse_scan(record))
            index += 1
        elif pe:
            pe = False
            endstep = int(stripped)

    return {'records': records, 'timestamps': timestamps, 'amount_of_records': index, 'endstep': endstep}

# Convert parsed records to a 2D array
def calculate_distances(records, amount_of_records, endstep):
    if endstep is not None:
        return np.array(records).reshape((amount_of_records, endstep + 1))
    else:
        exit('No endStep given in ubh file')

# Print the results of a trace
def print_trace_simple(trace):
    for item in trace:
        print("{} at {}ms".format(item[1], item[0]))

    print("Timespan: {}".format(calculate_trace_timespan(trace)))
    print("Distance: {}".format(calculate_trace_distance(trace)))
    print("Average velocity: {}".format(calculate_velocity(trace)))

# Calculate the timespan of a trace
def calculate_trace_timespan(trace):
    start = trace[0][0]
    end = trace[-1][0]
    return (end - start)

# Calculate the distance that is traveled in a trace 
# (only applicable to a trace of the front or the back)
def calculate_trace_distance(trace):
    start = trace[0][1][0]
    end = trace[-1][1][0]
    if start > 0:
        return start - end
    else:
        return abs(end) - abs(start)

# Make a trace of the beginning of the front of the train
def trace_beginning_of_train(coordinates, timestamps):
    result = []
    for i, row in enumerate(coordinates):
        # Front of the train
        last_item = row[-1]
        # If front of train has passed the y-axis, then stop
        if last_item[0] <= 0:
            return result
        # The front of the train is a bit further from the lidar
        elif last_item[1] > 3000:
            result.append((timestamps[i], last_item))
    return result

# Make a trace of the back of the train
def trace_back_of_train(coordinates, timestamps):
    result = []
    for i, row in enumerate(coordinates):
        first_item = row[0]
        if first_item[0] <= 0:
            result.append((timestamps[i], first_item))
    return result

# Calculate the velocity of a train in a front or back trace
def calculate_velocity(trace):
    distance = calculate_trace_distance(trace)
    timespan = calculate_trace_timespan(trace)
    avg_velocity = distance/timespan
    return avg_velocity

# Calculate the timespan of a whole recording
def calculate_total_timespan(timestamps):
    start = timestamps[0]
    end = timestamps[-1]
    return end - start

# Calculate the increase of velocity distributed over every scan of the recording
# The v1 and v2 are the velocity of the front and the backtrace
def calculate_accelleration_per_ms(v1, v2, timespan):
    return (v2 - v1) / (timespan)

# Open UBH file
with open('file2.ubh') as recording:
    # Parse recording for records, timestamps and the amount of records
    processed_recording = get_timestamps_and_scans(recording)
    records = processed_recording['records']
    timestamps = processed_recording ['timestamps']
    amount_of_records = processed_recording['amount_of_records']

    # Turn end result into a 2D matrix with i rows (amount of scans)
    # and 1081 cols (amount of snapshots in a scan)
    distances = calculate_distances(
            records, 
            amount_of_records,
            processed_recording['endstep']
        )
    
    # Calculate the coordinates for each distance
    coordinates = calculate_coordinates(distances)

    # Calculate the trace of the front of the train
    train_front_trace = trace_beginning_of_train(coordinates, timestamps)
    # Calculate the trace of the end of the train
    train_back_trace = trace_back_of_train(coordinates, timestamps)

    # Calculate the velocities of the front and the back trace of the train
    vel_front = calculate_velocity(train_front_trace)
    vel_back = calculate_velocity(train_back_trace)
    
    print(vel_front)
    print(vel_back)
    print(calculate_total_timespan(timestamps))

    # Calculate the increase of speed of the train in mm/ms^2 or m/s^2 for the whole recording
    acc_per_ms = calculate_accelleration_per_ms(vel_front, vel_back, calculate_total_timespan(timestamps))

    # Vars for the rendering of the image of the train
    colors = [(0,0,0)]
    area = np.pi*3

    app = QtWidgets.QApplication(sys.argv)

    # Iterate through each scan
    for i, scan in enumerate(coordinates):
        x_values = []
        y_values = []

        if i == 300:
            # Iterate through each coordinate in a scan
            for value in scan:
                # Since the train in the simulation is traveling right to left (pos x to neg x)
                # the offset needs to be added to the x value
                x_values.append(value[0]/1000)
                y_values.append(value[1]/1000)
        
            # Render an image of the accummulated image of all the coordinates
            pg.plot(x_values, y_values, pen=None, symbol='o')
            status = app.exec_()
            sys.exit(status)
    gc.collect()
