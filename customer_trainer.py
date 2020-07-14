import cv2
import numpy as np
from PIL import Image
import os

recognizer = cv2.face.LBPHFaceRecognizer_create()
faceCascade = cv2.CascadeClassifier("Cascades/haarcascade_frontalface_default.xml")


# function to get the images and label data
def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faceSamples = []
    image_ids = []
    for image_path in imagePaths:
        PIL_img = Image.open(image_path).convert('L')  # convert it to grayscale
        img_numpy_array = np.array(PIL_img, 'uint8')
        img_id = int(os.path.split(image_path)[-1].split(".")[1])
        faces = faceCascade.detectMultiScale(img_numpy_array)
        for (x, y, w, h) in faces:
            faceSamples.append(img_numpy_array[y:y + h, x:x + w])
            image_ids.append(img_id)
    return faceSamples, image_ids

def train_image_model():
    print("\nTraining the model...")
    faces, image_ids = getImagesAndLabels('dataset')
    recognizer.train(faces, np.array(image_ids))

    # Save the model into trainer directory named 'trainer.yml'
    recognizer.write('trainer/trainer.yml')
    print("\nTotal {0} faces trained.".format(len(np.unique(image_ids))))

# train_image_model()
