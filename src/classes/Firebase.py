from firebase_admin import firestore
from funcs.utils import *

import firebase_admin


class FirebaseDB:
    def __init__(self, token):
        cred = firebase_admin.credentials.Certificate(f'./{token}.json')
        firebase_admin.initialize_app(cred)

        self.db = firestore.client()


    def get_document_by_id(self, collection_name, document_id):
        collection_ref = self.db.collection(collection_name)

        doc_ref = collection_ref.document(document_id)
        doc_snapshot = doc_ref.get()

        if doc_snapshot.exists:
            return doc_snapshot.to_dict()
        else:
            return None
    

    def get_all_docs_in_collection(self, collection_name):
        collection_ref = self.db.collection(collection_name)

        docs = collection_ref.stream()

        all_docs = {}

        for doc in docs:
            doc_id = doc.id
            doc_data = doc.to_dict()
            all_docs[doc_id] = doc_data

        return all_docs


    def update_value_doc(self, doc_name, key, forecast_new_data):
        doc_ref = self.db.document(doc_name)
        doc_data = doc_ref.get().to_dict()
        
        if not doc_data:
            doc_ref.set({key: forecast_new_data})
        else:
            doc_data[key].update(forecast_new_data)
            doc_ref.update(doc_data)


    def send_forecast_to_db(self, spot_name, full_dict):
        spot_doc = self.db.collection('forecast_data').document(spot_name)
        pico_id_str = spot_doc.get().to_dict()['pico_id']
        
        for dt_original in full_dict.keys():
            small_dict = full_dict[dt_original]
            
            hour_str, day_str = parse_date_time(dt_original)
            small_dict['horario'] = hour_str
            small_dict['pico_id'] = pico_id_str

            doc_ref = spot_doc.collection(day_str).document(hour_str)
            doc_ref.set(small_dict)


    def send_history_to_db(self, spot_name, full_dict):
        self.update_value_doc(f'history_data/{spot_name}', 'forecast_history_data', full_dict)