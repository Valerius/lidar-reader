# Lidar reader
---

## Description
This command line application (CLA) reads UBH files, produced by a UTM-30LX-EW Lidar. The program is taylored specifically to process and render the image of a moving vehicle. The translations and operations on the data can be found in the help section of the CLA and this readme file. 

## Important
- This version of the CLA presupposes a connection to a remote database defined in db_connect.py;
- All distances are measured in millimeters;
- The Lidar distance points are converted to coordinates on a 2D Cartesian plane;
- The Lidar is to be found at the intersection of the x and y axes;
- The object is supposed to be moving from left to right;
- The object is supposed to be moving on a straight line, perpendicular to the camera;
- The object is supposed to be found within 4000mm from the camera.

## Modules
The application is devided into several modules/files with a functional distinction.
- reader.py: logic for the CLA;
- main.py: functions corresponding to the commands defined in the reader.py;
- parsing.py: code for parsing the UBH-file, converting distance points to coordinates;
- db_connect.py: connection to the remote database;
- pipeline.py: sending and fetching of parsed data;
- classes.py: data model and functions used for all the transformations and operations on the processed (parsed) data;
- clustering.py: clustering the processed data;
- rendering.py: creating images of the processed data.

## Installation
Make sure you have the Python3 language installed. Clone the repository. Dependencies can be installed by running:
pip3 install -r requirements.txt

## Execution
The command line application can be executed using python3 reader \[option\]. To display the help message, execute:
python3 reader --help

## Help