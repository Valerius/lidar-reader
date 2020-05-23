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
parser.add_argument('-pco', '--print-coordinates', help='get coordinates of distances in a ubh file', action='store_true')
# Option to render the scans belonging to a ubh file
parser.add_argument('-rs', '--render-scans', help='render scans belonging to a ubh file', action='store_true')
# # Option to render the scans belonging to a ubh file with clusters
parser.add_argument('-rc', '--render-clusters', help='render scans belonging to a ubh file with clusters', action='store_true')
# # Option to print distance between each scan
parser.add_argument('-rsd', '--render-scan-differences', help='render distance between each scan', action='store_true')
# Option to render all matching clusters
parser.add_argument('-rmc', '--render-matching-clusters', help='render all matching clusters', action='store_true')
# Option to render a complete image of the train
parser.add_argument('-rci', '--render-complete-image', help='render a compelete image of the train', action='store_true')
# Option to enter the program to enter commands
parser.add_argument('-ep', '--enter-program', help='enter program', action='store_true')


# Read arguments specified by user
args = parser.parse_args()

if args.parse_file:
  # Initialize file to write to
  with open('parse-file.txt', 'w') as f:
    with redirect_stdout(f):
      print(main.get_parsed_ubh_file())
elif args.print_coordinates:
  with open('coordinates.txt', 'w') as f:
    with redirect_stdout(f):
      print(main.print_coordinates())
elif args.render_scans:
  main.render_scans()
elif args.render_clusters:
  main.render_clusters()
elif args.render_scan_differences:
  main.render_scan_differences()
elif args.render_matching_clusters:
  main.render_matching_clusters()
elif args.render_complete_image:
  main.render_complete_image()
elif args.enter_program:
  main.enter_program()


