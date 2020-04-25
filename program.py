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

def calculate_angle(index):
    return m.radians(135 - index * 0.25)

def calculate_x_coordinate(distance, angle):
    return distance * m.sin(angle)

def calculate_y_coordinate(distance, angle):
    return distance * m.cos(angle)

def calculate_coordinate(distance, index):
    angle = calculate_angle(index)
    x_coordinate = calculate_x_coordinate(distance, angle)
    y_coordinate = calculate_y_coordinate(distance, angle)
    return (x_coordinate, y_coordinate)

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

def calculate_distances(records, amount_of_records, endstep):
    if endstep is not None:
        return np.array(records).reshape((amount_of_records, endstep + 1))
    else:
        exit('No endStep given in ubh file')

def print_trace_simple(trace):
    for item in trace:
        print("{} at {}ms".format(item[1], item[0]))

    print("Timespan: {}".format(calculate_trace_timespan(trace)))
    print("Distance: {}".format(calculate_trace_distance(trace)))

def calculate_trace_timespan(trace):
    start = trace[0][0]
    end = trace[-1][0]
    return end - start

def calculate_trace_distance(trace):
    start = trace[0][1][0]
    end = trace[-1][1][0]
    if start > 0:
        return start - end
    else:
        return end - start

# Open UBH file
with open('file.ubh') as recording:
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
    coordinates = calculate_coordinates(distances)











    # Collection of points of the front of the train until it reaches the y-axis
    train_front_trace = trace_beginning_of_train(coordinates, timestamps)
    print_trace_simple(train_front_trace)
    # Approximately the moment the train hits the y-axis
    last_front_trace = train_front_trace[-1]
    # Time in milliseconds the train needs to reach the y-axis
    total_time_interval = last_front_trace[0] - train_front_trace[0][0]
    speeds = []

    # Calculate the speed of the train at each given snapshot
    for item in train_front_trace:
        # millimeters
        distance = item[1][0] - last_front_trace[1][0]
        # milliseconds
        time_interval = last_front_trace[0] - item[0]
        if time_interval != 0:
            # Speed in m/s
            speed = distance/time_interval
            speeds.append((speed, time_interval))

    average_accelleration = (speeds[-1][0] - speeds[0][0]) / (total_time_interval / 1000)
    #1475

