import firebase_admin
from firebase_admin import credentials, firestore


firebase_admin.initialize_app()
db = firestore.client()  # this connects to our Firestore database


def addData(link,data):
  if not firebase_admin._apps:
        firebase_admin.initialize_app()
  db.collection(u'Summarizer').document(str(link)).set(data)

def getData(link):
  if not firebase_admin._apps:
        firebase_admin.initialize_app()
  collection = db.collection('Audio_to_text')
  doc = collection.document(link)
  res = doc.get().to_dict()
  return res
