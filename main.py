import os
import customer_dataset
import customer_trainer
import customer_recognition


# main menu function
def mainMenu():
    print("\t**********************************************")
    print("\t********** Customer Tracking System **********")
    print("\t**********************************************\n")
    print("[1] Capture Customer Images")
    print("[2] Train Model")
    print("[3] Recognize Customer")
    print("[4] Exit")

    while True:
        try:
            choice = int(input("Enter Choice: "))
            if choice == 1:
                CaptureNewFacesForDataset()
                break
            elif choice == 2:
                TrainModelForNewFaces()
                break
            elif choice == 3:
                RecognizeFacesForCustomers()
                break
            elif choice == 4:
                print("Application Closed...")
                break
            else:
                print("Invalid Choice. Enter 1-4")
                mainMenu()
        except ValueError:
            print("Invalid Choice. Enter 1-4")
    exit


# -----------------------------------------------------------------------
# calling the capture_images method form capture customer_dataset.py file
def CaptureNewFacesForDataset():
    customer_dataset.capture_images()
    key = input("Enter any key to return main menu")
    mainMenu()


# --------------------------------------------------------------------------------------------------------------
# calling the train_image_model method from train_model.py file to train model based on faces in dataset folder
def TrainModelForNewFaces():
    customer_trainer.train_image_model()
    key = input("Enter any key to return main menu")
    mainMenu()


# ------------------------------------------------------------------------------------------
# calling the recognize_customer method from recognize_customer.py file to identify customer
def RecognizeFacesForCustomers():
    customer_recognition.recognize_customer()
    key = input("Enter any key to return main menu")
    mainMenu()


# ---------------calling main menu------------------
mainMenu()
