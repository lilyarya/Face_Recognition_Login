from base64 import b64decode
import os
import pickle  

def register_on_submit(email, image):
    header, encoded = image.split(",", 1)

    with open("Registering.png", "wb") as f:
        f.write(b64decode(encoded))
    
    try:
        try:
            data = pickle.loads(open("data.pickle", "rb").read())
        except Exception as e:
            print(e.__cause__)
            data = dict()
            with open("data.pickle", "wb") as f:
                f.write(pickle.dumps(data))
        
        data = pickle.loads(open("data.pickle", "rb").read())
        if email in data.keys():
            return "Email id already registered"
        data[email] = encoded
        with open("data.pickle", "wb") as f:
            f.write(pickle.dumps(data))
    except Exception as e:
        print(e.__cause__)
        return "Registration failed!"
    return "Registration Successful!"