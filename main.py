# Import local modules
import parsing
from classes import *

# Get a parsed ubh file
def get_parsed_ubh_file():
  # Open UBH file
  with open('file2.ubh') as recording:
    # Parse recording for records, timestamps and the amount of records
    return parsing.get_timestamps_and_scans(recording)

def get_distances(processed_recording):
  return parsing.calculate_distances(
    processed_recording['records'], 
    processed_recording['amount_of_records'],
    processed_recording['endstep']
  )

def get_coordinates(processed_recording):
  distances = get_distances(processed_recording)
  return parsing.calculate_coordinates(distances)

def get_recording():
  processed_recording = get_parsed_ubh_file()
  coordinates = get_coordinates(processed_recording)
  return Recording(coordinates, processed_recording['timestamps'])

def render_scans():
  recording = get_recording()
  amount = recording.render_scans()
  print('Success! %d scans rendered' % amount)

def render_clustered_scans():
  recording = get_recording()
  amount = recording.render_clustered_scans()
  print('Success! %d clustered scans rendered' % amount)

def print_centroids():
  recording = get_recording()
  recording.get_centroids() 
  for scan_centroids in recording.centroids:
    print(scan_centroids)

def print_centroid_differences():
  recording = get_recording()
  recording.get_centroids()
  results = recording.get_minimal_centroid_differences()
  for result in results:
    print(result)

def print_matching_clusters():
  recording = get_recording()
  recording.get_centroids()
  results = recording.get_matching_clusters()
  for result in results:
    print(result)


