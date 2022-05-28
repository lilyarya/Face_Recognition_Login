from base64 import b64decode
import face_recognition as fr
import time
import os
import pickle  

"""

1.base64.b64decode() method, we are able to get the decoded string which can be in binary form .
2.The pickle module implements binary protocols for serializing and de-serializing a Python object structure.
3.The OS module in Python provides functions for interacting with the operating system. 
  OS comes under Python's standard utility modules.
  This module provides a portable way of using operating system-dependent functionality.

"""

def login_check(email, image):
    face_match = 0
    header, encoded = image.split(",", 1) # split image in given size

    with open("New.png", "wb") as f: #the “with” statement to read a file into Python
        f.write(b64decode(encoded))  #with statement to write some text out to a file

    data = pickle.loads(open("data.pickle", "rb").read()) 
 #pickle.loads is used to load pickled data from a bytes string.

    if email not in data.keys():
        return "This user ID is not registered yet"

    with open("Existing.png", "wb") as f:
        f.write(b64decode(data[email]))



    
    
    try:
        try:
            got_image = fr.load_image_file("New.png")
            existing_image = fr.load_image_file("Existing.png")
        except Exception as e:
            # print(e.__cause__)
            return "Data does not exist !"

        face_locations = fr.face_locations(got_image) # face_locations is an array listing the co-ordinates of each face!
        if(len(face_locations)==0):  #face_locations – Optionally provide a list of face locations to check.
            return "No face detected"
        if(len(face_locations)>1):
            return "Multiple faces detected"
            
        got_image_facialfeatures = fr.face_encodings(got_image)[0]
        existing_image_facialfeatures = fr.face_encodings(existing_image)[0]
        #face_encoding contains a universal 'encoding' of facial features that can be compared to any other picture of a face!
        results = fr.compare_faces([existing_image_facialfeatures], got_image_facialfeatures)
        if(results[0]):
            return "Successfully Logged in"
        else:
            return "User ID and face doesn't match!"
    except Exception as e:
        # print(e.__cause__)
        return "Image not clear ! Please try again !"