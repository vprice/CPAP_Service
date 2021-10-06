import mysql.connector

try:
    connection = mysql.connector.connect(
        host="localhost",
        port="3306",
        user="root",
        password=input("What password to connect with: "),
        database="information")
except:
    print("Error: Could not connect to MySQL db.")
    exit()

cursor = connection.cursor()


cursor.execute('''
          CREATE TABLE IF NOT EXISTS therapy_hours
          (id INT AUTO_INCREMENT PRIMARY KEY NOT NULL, 
           patient_id VARCHAR(255) NOT NULL,
           device_id VARCHAR(255) NOT NULL,
           therapy_hours DOUBLE NOT NULL,
           timestamp VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')

cursor.execute('''
          CREATE TABLE IF NOT EXISTS AHI_score
          (id INT AUTO_INCREMENT PRIMARY KEY NOT NULL, 
           patient_id VARCHAR(250) NOT NULL,
           device_id VARCHAR(250) NOT NULL,
           AHI_score DOUBLE NOT NULL,
           timestamp VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')
connection.commit()
connection.close()