import mysql.connector

try:
    connection = mysql.connector.connect(
        host="cpap-lab6.eastus.cloudapp.azure.com",
        port="3306",
        user="user",
        password="password",
        database="information")
except:
    print("Error: Could not connect to MySQL db.")
    exit()

cursor = connection.cursor()
cursor.execute('''DROP TABLE therapy_hours''')
cursor.execute('''DROP TABLE AHI_score''')

connection.commit()
connection.close()
