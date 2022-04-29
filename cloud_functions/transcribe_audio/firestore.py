import firebase_admin
from firebase_admin import firestore

firebase_admin.initialize_app()
db = firestore.client()  # this connects to our Firestore database
collection = db.collection('Audio_to_text')  # opens 'places' collection
doc = collection.document('link')  # specifies the 'rome' document

def addData(link,data):
    if not firebase_admin._apps:
        firebase_admin.initialize_app()
    db.collection(u'Audio_to_text').document(str(link)).set(data)

def getData(link):
    doc = collection.document(link)
    res = doc.get().to_dict()
    return res
