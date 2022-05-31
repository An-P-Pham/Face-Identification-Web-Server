import cv2
import os
import face_recognition
from pathlib import Path
import pymysql
import logging

#connect to database
connected = False
try:
    mydb = pymysql.connect("localhost", "root", "root", "face_files")
except pymysql.MySQLError as e:
    logging.error(e)
finally:
    mycursor = mydb.cursor()
    connected = True
    logging.info('Connection opened successfully.')


#path of our images
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
unknown_faces_dir = os.path.join(BASE_DIR, "unknown") #unknown faces directory
known_faces_dir = os.path.join(BASE_DIR, "known") #known faces directory
tolerance = 0.6 #used for identification
MODEL = "hog"

known_faces = []
known_names = []

def convertToBinaryData(filename):
    #Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

# checks if already exists in database
def checkExists(item_name):
    mycursor.execute(
        "SELECT fullname, COUNT(*) FROM faceid WHERE fullname = %s GROUP BY fullname",
        (item_name,)
    ) #SELECT EXISTS(SELECT 1 FROM mysql.user WHERE user = 'username')?
    # gets the number of rows affected by the command executed
    row_count = mycursor.rowcount
    if row_count == 0:
        return False
    else:
        return True


# add to database
def insert_data(fullname, photo):
        sqlFormula = "INSERT INTO faceid (fullname, photo) VALUES(%s, %s)"
        bin_photo = convertToBinaryData(photo)
        # Convert data into tuple format
        sql_person = (fullname, bin_photo)
        mycursor.execute(sqlFormula, sql_person)
        mydb.commit()


#if you want to retrieve the data
def get_data():
    query = "SELECT fullname, photo FROM faceid"
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    for x in myresult:
        curr_name = x[0]
        image = x[1]
        photo = curr_name + ".jpeg"
        print(curr_name)


def load_known():
    for root, dirs, files in os.walk(known_faces_dir):
        for file in files:
            if file.endswith("png") or file.endswith("jpg") or file.endswith('jpeg'):
                path = os.path.join(root, file)
                name = Path(path).stem
                if not checkExists(name) and connected: #loads into mysql_database if we don't have it yet
                    insert_data(name, path)
                image = face_recognition.load_image_file(path)
                encoding = face_recognition.face_encodings(image)[0]
                known_faces.append(encoding)
                known_names.append(name)


def detect_unknown():
    matched_faces = []
    for root, dirs, files in os.walk(unknown_faces_dir):
        for file in files:
            if file.endswith("png") or file.endswith("jpg") or file.endswith('jpeg'):
                path = os.path.join(root, file)
                image = face_recognition.load_image_file(path)
                locations = face_recognition.face_locations(image, model=MODEL)
                encodings = face_recognition.face_encodings(image, locations)
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                for face_encoding, face_location in zip(encodings, locations):
                    results = face_recognition.compare_faces(known_faces, face_encoding, tolerance) #return booleans
                    match = None
                    if True in results:
                        match = known_names[results.index(True)]
                        matched_faces.append(match)
                os.remove(path) #remove the file so we don't get multiple matches next time
    return matched_faces