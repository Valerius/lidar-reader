# Library for creating cli-applications
import argparse
# Import function to write to files
from contextlib import redirect_stdout

# Import local modules
import main

# Initialize cli application
parser = argparse.ArgumentParser()
# Option to parse ubh file
parser.add_argument('-pf', '--parse-file', help='parse a ubh-file', action='store_true')
# Option to get coordinates of distances in file
#parser.add_argument('-gc', '--get-coordinates', help='get coordinates of distances in a ubh file', action='store_true')
# Option to render the scans belonging to a ubh file
parser.add_argument('-rs', '--render-scans', help='render scans belonging to a ubh file', action='store_true')


# Read arguments specified by user
args = parser.parse_args()

if args.parse_file:
  # Initialize file to write to
  with open('parse-file.txt', 'w') as f:
    with redirect_stdout(f):
      print(main.get_parsed_ubh_file())
# elif args.get_coordinates:
#   with open('coordinates.txt', 'w') as f:
#     with redirect_stdout(f):
#       print(main.get_coordinates())
elif args.parse_file:
  main.render_scans()


