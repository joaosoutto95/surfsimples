import argparse

from pytz import timezone
from configs import FIREB_NAME_JSON, NUMB_DAYS, BRAZIL_TZ
from funcs.utils import *
from funcs.tide import *
from classes.Firebase import FirebaseDB


db = FirebaseDB(FIREB_NAME_JSON)

parser = argparse.ArgumentParser(description='Process and send surfing forecast data.')
parser.add_argument('-d', '--disable_email', action='store_true', help='Disable sending email')
args = parser.parse_args()

year_now = dt.datetime.now(timezone(BRAZIL_TZ)).replace(tzinfo=None, microsecond=0).year

local_list, local_coll_docs = db.get_spots_names()

for local in local_list:
    doc_spot = [doc.to_dict() for doc in local_coll_docs if doc.id == local][0]
    doc_hardcoded = db.get_all_docs_in_collection('hardcoded_jsons')
    doc_tide = db.get_document_by_id('tide_stations_data', doc_spot['ref_marinha_tide']).get(f'tide_{year_now}')

    lat, lon = doc_spot['lat'], doc_spot['lon']
    wave_json = stormglass_request(lat, lon, NUMB_DAYS)
    tide_json = get_tide_forecasts(doc_tide, doc_hardcoded['tide_specs'], NUMB_DAYS)

    t = 0
    while (wave_json==None) and (t<3):
        wave_json = stormglass_request(lat, lon, NUMB_DAYS)
        t+=1

    if wave_json:
        df_full_forecast = data_to_pandas(wave_json, tide_json, doc_hardcoded, doc_spot['beach_normal_degree'])

        dict_full_forecast = df_full_to_dict(df_full_forecast)

        db.send_forecast_to_db(local, dict_full_forecast)
        db.send_history_to_db(local, dict_full_forecast)

    else:
        print('API Request failed.')