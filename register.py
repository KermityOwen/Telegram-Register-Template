import mysql.connector
import os

HOST = os.getenv("HOST")
USER = os.getenv("USER")
PW = os.getenv("PASSWORD")

mydb = mysql.connector.connect(
    host=HOST,
    user=USER,
    password=PW,
    database="d_morgentaler"
)

mycursor = mydb.cursor()


def create_helper(name, lat, long, id):
    sql = "INSERT INTO helpers (name, latitude, longitude, uid) VALUES (%s, %s, %s, %s)"
    values = (name, lat, long, id)
    mycursor.execute(sql, values)
    mydb.commit()
    print("done")



# mycursor.execute("CREATE TABLE helpers (name VARCHAR(255), latitude FLOAT(7, 5), longitude FLOAT(8, 5))")

print("ok")

