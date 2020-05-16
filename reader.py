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
# parser.add_argument('-rs', '--render-scans', help='render scans belonging to a ubh file', action='store_true')
# # Option to render the scans belonging to a ubh file with clusters
# parser.add_argument('-rc', '--render-clusters', help='render scans belonging to a ubh file with clusters', action='store_true')
# # Option to print centroids for each scan cluster
# parser.add_argument('-pc', '--print-centroids', help='print centroids for each scan cluster', action='store_true')
# # Option to print minimal centroid differences for each scan
# parser.add_argument('-pcd', '--print-centroid-differences', help='print minimal centroid differences for each scan', action='store_true')
# # Option to print all matching clusters
# parser.add_argument('-pmc', '--print-matching-clusters', help='print all matching clusters', action='store_true')
parser.add_argument('-ep', '--enter-program', help='enter program', action='store_true')


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
elif args.enter_program:
  main.enter_program()


