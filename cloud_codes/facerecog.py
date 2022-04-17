from skimage import io
import face_recognition
import os
import glob
import numpy as np

import json
face_rec_api = "http://Dgital_Eye.azurewebsites.net/face_recognition"
class SimpleFacerec:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []

        self.frame_resizing = 0.25

    def load_encoding_images(self, images_path):
        """
        Load encoding images from path
        :param images_path:
        :return:
        """
        
        images_path = glob.glob(os.path.join(images_path, "*.*"))

        print("{} encoding images found.".format(len(images_path)))

        
        for img_path in images_path:
            img = io.imread(img_path)
            #rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            
            basename = os.path.basename(img_path)
            (filename, ext) = os.path.splitext(basename)
            
            img_encoding = face_recognition.face_encodings(img)[0]

            
            self.known_face_encodings.append(img_encoding)
            self.known_face_names.append(filename)
        print("Encoding images loaded")

    def detect_known_faces(self, frame):
        
        rgb_small_frame=frame
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"

           
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]
            face_names.append(name)

        
        face_locations = np.array(face_locations)
        face_locations = face_locations / self.frame_resizing
        return face_locations.astype(int), face_names

    

def recog(img):
    img1=io.imread(img)
    sfr=SimpleFacerec()
    sfr.load_encoding_images("images/")
    faceloc,facename=sfr.detect_known_faces(img1)
    for fl,fn in zip(faceloc,facename):
        face_name=fn
        return(face_name)
