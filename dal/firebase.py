import os
from decouple import config as envs
import pyrebase


class Firebase:
    def __init__(self):    
        config = {
            'apiKey': envs('FB_API_KEY'),
            'serverKey': envs('FB_SERVER_KEY'),
            'authDomain': envs('FB_AUTH_DOMAIN'),
            'databaseURL': envs('FB_DB_URL'),
            'storageBucket': envs('FB_ST_BUCKET'),
            'messagingSenderId': envs('FB_MSS_SND_ID'),
            'projectId': envs('FB_PROJ_ID'),
            'serviceAccount': envs('FB_SERVICE_PK_PATH'),
        }
        firebase = pyrebase.initialize_app(config)

        self.db = firebase.database()
        self.pictures = self.db.child('pictures')
        self.pictures_document = self.pictures.get().val()


    def get_pictures(self):
        pictures_list = [
            self.pictures_document[e] for e in list(self.pictures_document.keys())]
        return pictures_list


    def get_last_picture(self):
        return self.get_pictures()[-1]
    

    def push_picture(self, picture):
        self.db.child('pictures').push(picture)

    
    def picture_exists(self, picture):
        return picture in self.get_pictures()


fb = Firebase()
