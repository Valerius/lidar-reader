# Import local modules
import parsing
from classes import *

# Get a parsed ubh file
def get_parsed_ubh_file():
  # Open UBH file
  with open('file.ubh') as recording:
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

def print_coordinates():
  processed_recording = get_parsed_ubh_file()
  return get_coordinates(processed_recording)

def get_recording():
  processed_recording = get_parsed_ubh_file()
  coordinates = get_coordinates(processed_recording)
  return Recording(coordinates, processed_recording['timestamps'])

def enter_program():
  recording = get_recording()
  pdb.set_trace()

def render_scans():
  recording = get_recording()
  recording.scan().scan_list.render()

def render_clusters():
  recording = get_recording()
  recording.cluster().scan_list.render()

def render_scan_differences():
  recording = get_recording()
  recording.cluster().scan_list.render_delta_matches()

def render_matching_clusters():
  recording = get_recording()
  recording.cluster().scan_list.render_matches()

def render_complete_image():
  recording = get_recording()
  recording.cluster().scan_list.render_complete()
