# db library
import pyodbc 

#write the password and user name yourself, dont forget to remove before pushing
conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=tcp:;'
                      'Port=;'
                      'Database=;'
                      'UID=;'
                      'PWD=;')

cursor = conn.cursor()
