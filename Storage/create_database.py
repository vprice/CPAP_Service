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
          (id INT AUTO_INCREMENT PRIMARY KEY , 
           patient_id VARCHAR(255),
           device_id VARCHAR(255),
           therapy_hours DOUBLE,
           timestamp VARCHAR(100),
           date_created VARCHAR(100))
          ''')

cursor.execute('''
          CREATE TABLE IF NOT EXISTS AHI_score
          (id INT AUTO_INCREMENT PRIMARY KEY , 
           patient_id VARCHAR(250),
           device_id VARCHAR(250),
           AHI_score DOUBLE,
           timestamp VARCHAR(100),
           date_created VARCHAR(100))
          ''')
connection.commit()
connection.close()