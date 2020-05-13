# Stats library
import numpy as np
# Math library
import math as m

# Parse a scan (one rotation recording by the lidar), extracting the distance (x)
def parse_scan(line):
    result = []
    row = line.split(';')
    for item in row:
        result.append(float(item.split('|')[0]))
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
