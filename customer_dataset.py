import datetime
import time
import cv2
import mysql.connector
from mysql_connection import mydb
from mysql.connector import Error
import os


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData


def add_customer_into_db(c_name, c_phoneNo, c_address, c_temperature, c_img):
    try:
        cursor = mydb.cursor()
        sql = """INSERT INTO tbl_custmers(customer_name, customer_phoneNo, customer_address, customer_temperature, date, time, customer_image) VALUES(%s, %s, %s, %s, %s, %s, %s)"""

        photo = convertToBinaryData(c_img)
        ts = time.time()
        creation_date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%y')
        creation_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')

        val = (c_name, c_phoneNo, c_address, c_temperature, creation_date, creation_time, photo)

        cursor.execute(sql, val)
        mydb.commit()
        print(cursor.rowcount, "Customer Registered...")
    except mysql.connector.Error as error:
        print("Failed inserting customer data into MySQL table {}".format(error))

# starting video capture
def capture_images():
    cap = cv2.VideoCapture(1)
    cap.set(3, 640)  # set Width
    cap.set(4, 480)  # set Height
    font = cv2.FONT_HERSHEY_SIMPLEX

    # get id of last registered customer
    cursor = mydb.cursor()
    cursor.execute("SELECT customer_id FROM tbl_custmers")
    result = cursor.fetchall()
    if len(result) == 0:
        new_customer_id = 1
    else:
        for c_id in result:
            new_customer_id = int(c_id[0] + 1)

    # Set id for each customer
    print('\nNew Customer Id: ', new_customer_id)
    customer_name = input("Enter Customer Name: ")
    customer_phoneNo = input("Enter Contact Number: ")
    customer_address = input("Enter Address: ")
    try:
        customer_temperature = float(input("Enter Customer Current Body Temperature: "))
    except:
        print('Invalid Value...Try Again')
        return

    if is_number(new_customer_id) and customer_name.isalpha() and isinstance(customer_temperature, float) and not "".__eq__(customer_phoneNo) and not "".__eq__(customer_address):
        print("\nLook at the camera and wait for capturing images for dataset...")
        count = 0  # customer dataset count
        lef_counter = right_counter = up_counter = down_counter = front_counter = feature_counter = 0
        lef_counter_trigger = right_counter_trigger = up_counter_trigger = down_counter_trigger = front_counter_trigger = False

        faceCascade = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')

        while True:
            ret, img = cap.read()
            img = cv2.flip(img, 1)  # Flip video frame vertically
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, 1.3, 5)

            cv2.putText(img, "F: Front Capture: ", (20, 300), font, 0.6, (0, 255, 0), 1, cv2.LINE_AA)
            cv2.putText(img, "A: Bend Left", (20, 330), font, 0.6, (0, 255, 0), 1, cv2.LINE_AA)
            cv2.putText(img, "D: Bend Right", (20, 360), font, 0.6, (0, 255, 0), 1, cv2.LINE_AA)
            cv2.putText(img, "W: Chen Up", (20, 390), font, 0.6, (0, 255, 0), 1, cv2.LINE_AA)
            cv2.putText(img, "S: Chen Down", (20, 420), font, 0.6, (0, 255, 0), 1, cv2.LINE_AA)
            cv2.imshow('Customer Tracking Systm', img)
            k = cv2.waitKey(10)

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                # Press 'F' to Capture Featured Image for Customer Profile
                if k == 102 or front_counter_trigger:
                    if feature_counter == 0:
                        cv2.imwrite("featured images/" + customer_name + "." + str(new_customer_id) + ".jpg", gray[y:y + h, x:x + w])
                        feature_counter += 1

                    front_counter_trigger = True
                    if not front_counter == 20:
                        cv2.imwrite("dataset/" + customer_name + "." + str(new_customer_id) + "." + str(count) + ".jpg", gray[y:y + h, x:x + w])
                        count += 1
                        front_counter += 1
                    else:
                        front_counter_trigger = False
                        print('All Front Face Saved...')

                # Press 'a' to capture left bended face
                if k == 97 or lef_counter_trigger:
                    lef_counter_trigger = True
                    if not lef_counter == 20:
                        cv2.imwrite("dataset/" + customer_name + "." + str(new_customer_id) + "." + str(count) + ".jpg", gray[y:y + h, x:x + w])
                        count += 1
                        lef_counter += 1
                    else:
                        lef_counter_trigger = False
                        print('All left banded face saved...')

                # Press 'd' to capture right bended face
                if k == 100 or right_counter_trigger:
                    right_counter_trigger = True
                    if not right_counter == 20:
                        cv2.imwrite("dataset/" + customer_name + "." + str(new_customer_id) + "." + str(count) + ".jpg", gray[y:y + h, x:x + w])
                        count += 1
                        right_counter += 1
                    else:
                        right_counter_trigger = False
                        print('All right banded face saved...')

                # Press 's' to capture chin down face
                if k == 115 or down_counter_trigger:
                    down_counter_trigger = True
                    if not down_counter == 20:
                        cv2.imwrite("dataset/" + customer_name + "." + str(new_customer_id) + "." + str(count) + ".jpg", gray[y:y + h, x:x + w])
                        count += 1
                        down_counter += 1
                    else:
                        down_counter_trigger = False
                        print('All Chin Downed face saved...')

                # Press 'w' to capture chin up face
                if k == 119 or up_counter_trigger:
                    up_counter_trigger = True
                    if not up_counter == 20:
                        cv2.imwrite("dataset/" + customer_name + "." + str(new_customer_id) + "." + str(count) + ".jpg", gray[y:y + h, x:x + w])
                        count += 1
                        up_counter += 1
                    else:
                        up_counter_trigger = False
                        print('All Chin Up face saved...')

            if k == 27:
                break
            elif count >= 100:  # Take 100 face samples and stop video
                # add customer data into database
                customer_img = os.getcwd() + '\\featured images\\' + customer_name + "." + str(new_customer_id) + ".jpg"
                add_customer_into_db(customer_name, customer_phoneNo, customer_address, str(customer_temperature), customer_img)
                break

        cap.release()
        cv2.destroyAllWindows()
    else:
        if (is_number(new_customer_id)):
            print("Enter Alphabetical Name")
        if (customer_name.isalpha()):
            print("Enter Numeric ID")

# capture_images()