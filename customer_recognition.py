import datetime
import time
import mysql.connector
from mysql_connection import mydb
from mysql.connector import Error
import cv2
import numpy as np
import os
import tkinter as tk
from tkinter import simpledialog
import threading

cc = 0
def insert_customer_visit_details(c_id):
    global cc
    cc += 1
    c_temperature = 0.0
    isvalidEntry = False
    try:
        ts = time.time()
        visit_date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%y')
        visit_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')

        cursor = mydb.cursor()
        cursor.execute("SELECT visit_date, visit_time FROM tbl_customers_tracking WHERE customer_id='" + str(c_id) + "'")
        result = cursor.fetchall()

        if not len(result) == 0:
            r = result[len(result)-1]
            if r[0].__eq__(visit_date):
                hh = r[1].split(':')[0]
                if not hh.__eq__(visit_time.split(':')[0]):
                    isvalidEntry = True
                    try:
                        temperature = float(input("Enter Customer Current Body Temperature: "))
                    except:
                        print('Invalid Value...Try Again')
                        return
                    if temperature is not None:
                        c_temperature = temperature
            else:
                isvalidEntry = True
                try:
                    temperature = float(input("Enter Customer Current Body Temperature: "))
                except:
                    print('Invalid Value...Try Again')
                    return
                if temperature is not None:
                    c_temperature = temperature
        else:
            isvalidEntry = True
            try:
                temperature = float(input("Enter Customer Current Body Temperature: "))
            except:
                print('Invalid Value...Try Again')
                return
            if temperature is not None:
                c_temperature = temperature

        if isvalidEntry:
            cursor = mydb.cursor()
            sql = """INSERT INTO tbl_customers_tracking(customer_id, customer_temperature, visit_date, visit_time) VALUES(%s, %s, %s, %s)"""

            val = (c_id, c_temperature, visit_date, visit_time)

            cursor.execute(sql, val)
            mydb.commit()
            print(cursor.rowcount, "Customer Visit details stored...")
            cc = 0

    except mysql.connector.Error as error:
        print("Failed inserting customer data into MySQL table {}".format(error))
        cc = 0


def recognize_customer():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    # reading trained model
    recognizer.read('trainer/trainer.yml')
    cascadePath = 'Cascades/haarcascade_frontalface_default.xml'
    faceCascade = cv2.CascadeClassifier(cascadePath)

    font = cv2.FONT_HERSHEY_SIMPLEX
    id = 0
    cursor = mydb.cursor()
    cursor.execute("SELECT customer_id, customer_name FROM tbl_custmers")
    result = cursor.fetchall()

    cam = cv2.VideoCapture(1)  # starting video capture
    cam.set(3, 640)  # set width
    cam.set(4, 480)  # set height

    # Define min window size to be recognized as a face
    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)

    while True:
        ret, img = cam.read()
        img = cv2.flip(img, 1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # crop the face from video and convert into gray face image
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(int(minW), int(minH)),)

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

            # if confidence is < 100, Then '0' is perfect match
            if (confidence < 90):
                # id = names[id]
                for r in result:
                    if id in r:
                        c_id = r[0]
                        c_name = r[1]

                tt = str(id) + "-" + c_name
                confidence = "  {0}%".format(round(100 - confidence))
                t1 = threading.Thread(target=insert_customer_visit_details, args=(id,))
                global cc
                if cc == 0:
                    t1.start()
                    print('Process End')
                # insert_customer_visit_details(id)

            else:
                id = "Unknown"
                tt = id
                confidence = "  {0}%".format(round(100 - confidence))

            cv2.putText(img, str(tt), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
            cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

        cv2.imshow('Camera', img)

        k = cv2.waitKey(10) & 0xff  # Press 'ESC' to exit
        if k == 27:
            break

    cam.release()
    cv2.destroyAllWindows()

# recognize_customer()