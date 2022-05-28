from base64 import b64decode
import os
import pickle  
import face_recognition as fr
"""

1.base64.b64decode() method, we are able to get the decoded string which can be in binary form .
2.The pickle module implements binary protocols for serializing and de-serializing a Python object structure.
 “Pickling” is the process whereby a Python object hierarchy is converted into a byte stream, 
  and “unpickling” is the inverse operation, whereby a byte stream (from a binary file or bytes-like object)
  is converted back into an object hierarchy

"""


def register_on_submit(email, image):
    header, encoded = image.split(",", 1) # split image in given size

    with open("Registering.png", "wb") as f:  #the “with” statement to read a file into Python
        f.write(b64decode(encoded)) #with statement to write some text out to a file
    
    try:
        try:
            data = pickle.loads(open("data.pickle", "rb").read())
            #pickle.loads is used to load pickled data from a bytes string.
            #The "s" in loads refers to the fact that in Python 2, the data was loaded from a string.
        except Exception as e:
            # print(e.__cause__)
            data = dict()
            with open("data.pickle", "wb") as f:
                f.write(pickle.dumps(data))
        
        data = pickle.loads(open("data.pickle", "rb").read())

        if email in data.keys():
            return "This user ID is already registered"

        got_image = fr.load_image_file("Registering.png")
        face_locations = fr.face_locations(got_image) # face_locations is an array listing the co-ordinates of each face!
        if(len(face_locations)==0):
            return "No face detected"
        if(len(face_locations)>1):
            return "Multiple faces detected"

        data[email] = encoded # if face detected no multiple faces detected, store it in the dictionary
        with open("data.pickle", "wb") as f:
            f.write(pickle.dumps(data))
    except Exception as e:
        # print(e.__cause__)
        return "Registration failed !"
    return "Registration Successful"