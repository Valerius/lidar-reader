# db library
import pyodbc 

conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=tcp:62.194.254.144;'
                      'Port=1433;'
                      'Database=NSLiDAR;'
                      'UID=hicham;'
                      'PWD=TheHomies2020;')

cursor = conn.cursor()
