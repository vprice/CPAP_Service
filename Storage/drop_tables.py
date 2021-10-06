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
cursor.execute('''DROP TABLE therapy_hours''')
cursor.execute('''DROP TABLE AHI_score''')

connection.commit()
connection.close()
