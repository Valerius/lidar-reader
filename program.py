# Functionality to open files
import os
# Stats library
import numpy as np
# For debugging purposes
import pdb
# Math library
import math as m
# Import plotting library
import matplotlib.pyplot as plt

# This function parses scans (one rotation recording by the lidar)
def parse_scan(line):
    result = []
    row = line.split(';')
    for item in row:
        result.append(float(item.split('|')[0]))
    return result

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
    print("Average velocity: {}".format(calculate_velocity(trace)))

def calculate_trace_timespan(trace):
    start = trace[0][0]
    end = trace[-1][0]
    return (end - start)

def calculate_trace_distance(trace):
    start = trace[0][1][0]
    end = trace[-1][1][0]
    if start > 0:
        return start - end
    else:
        return abs(end) - abs(start)

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

def trace_back_of_train(coordinates, timestamps):
    result = []
    for i, row in enumerate(coordinates):
        first_item = row[0]
        if first_item[0] <= 0:
            result.append((timestamps[i], first_item))
    return result

def calculate_velocity(trace):
    distance = calculate_trace_distance(trace)
    timespan = calculate_trace_timespan(trace)
    avg_velocity = distance/timespan
    return avg_velocity

def calculate_total_timespan(timestamps):
    start = timestamps[0]
    end = timestamps[-1]
    return end - start

def calculate_accelleration(v1, v2, timespan):
    return (v2 - v1) / (timespan / 1000)

def get_total_distance(start, end):
    print(start)
    print(end)
    return abs(end - start)

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

    train_front_trace = trace_beginning_of_train(coordinates, timestamps)
    #print_trace_simple(train_front_trace)
    front_trace_timespan = calculate_trace_timespan(train_front_trace)
    front_trace_distance = calculate_trace_distance(train_front_trace)
    incrementation_per_scan = front_trace_distance / (front_trace_timespan / 25)

    x_values = []
    y_values = []


    for scan in coordinates:
        offset = 0
        for j, value in enumerate(reversed(scan)):
            if j < 1:
                offset = offset - value[0]
            if value[0] > 0:
                x_values.append(value[0] - offset)
            else:
                x_values.append(value[0] + offset)   

            y_values.append(value[1])
    
    colors = [(0,0,0)]
    area = np.pi*3

    # Plot
    plt.scatter(x_values, y_values, s=area, c=colors, alpha=0.5)
    plt.title('Scatter plot pythonspot.com')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()



    # train_back_trace = trace_back_of_train(coordinates, timestamps)
    # print_trace_simple(train_back_trace)

    # print("Total timespan: {}".format(total_timespan(timestamps)))
    # print("Avg. accelleration: {}".format(calculate_accelleration(calculate_velocity(train_front_trace), calculate_velocity(train_back_trace), total_timespan(timestamps))))

