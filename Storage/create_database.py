import sqlite3

connection = sqlite3.connect('information.db')
cursor = connection.cursor()
cursor.execute(' PRAGMA foreign_keys=ON; ')

cursor.execute('''
          CREATE TABLE IF NOT EXISTS therapy_hours
          (id INTEGER PRIMARY KEY ASC, 
           patient_id VARCHAR(250) NOT NULL,
           device_id VARCHAR(250) NOT NULL,
           therapy_hours REAL NOT NULL,
           timestamp VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')

cursor.execute('''
          CREATE TABLE IF NOT EXISTS AHI_score
          (id INTEGER PRIMARY KEY ASC, 
           patient_id VARCHAR(250) NOT NULL,
           device_id VARCHAR(250) NOT NULL,
           AHI_score REAL NOT NULL,
           timestamp VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')
connection.commit()
connection.close()