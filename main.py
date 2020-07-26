# Import local modules
import parsing
from classes import *
import numpy as np
import db_connect as db

# Get a parsed ubh file
def get_parsed_ubh_file():
  # Open UBH file
  with open('file1.ubh') as recording:
    # Parse recording for records, timestamps and the amount of records
    return parsing.get_timestamps_and_scans(recording)

def get_distances(processed_recording):
  return parsing.calculate_distances(
    processed_recording['records'], 
    processed_recording['amount_of_records'],
    processed_recording['endstep']
  )

def get_coordinates_and_angles(processed_recording):
  distances = get_distances(processed_recording)
  return parsing.calculate_coordinates_and_angles(distances)

def print_coordinates():
  processed_recording = get_parsed_ubh_file()
  return np.array(get_coordinates_and_angles(processed_recording)['coordinates'])

def get_recording():
  processed_recording = get_parsed_ubh_file()
  coordinates_and_angles = get_coordinates_and_angles(processed_recording)
  return Recording(
    coordinates_and_angles['coordinates'], 
    coordinates_and_angles['angles'], 
    processed_recording['timestamps'],
    coordinates_and_angles['indexes']
  )

def get_recording_from_db():
  recording_record = db.cursor.execute("select * from UBH_recording").fetchone()
  processed_recording = parsing.get_distances_from_db(recording_record)
  coordinates_and_angles = parsing.calculate_coordinates_and_angles(processed_recording['records'])

  return Recording(
    coordinates_and_angles['coordinates'], 
    coordinates_and_angles['angles'], 
    processed_recording['timestamps'],
    coordinates_and_angles['indexes']
  )

def enter_program():
  pdb.set_trace()

def render_scans():
  get_recording().scan_list.render()

def render_clusters():
  get_recording().scan_list.render_clusters()

def render_scan_differences():
  get_recording().scan_list.render_deltas()

def render_matching_clusters():
  get_recording().scan_list.render_matches()

def render_complete_image():
  get_recording().scan_list.render_complete()
