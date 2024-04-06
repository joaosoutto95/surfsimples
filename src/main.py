import argparse

from configs import FIREB_NAME_JSON, NUMB_DAYS, LOCAL
from funcs.utils import *
from funcs.tide import *
from classes.Firebase import FirebaseDB


db = FirebaseDB(FIREB_NAME_JSON)

parser = argparse.ArgumentParser(description='Process and send surfing forecast data.')
parser.add_argument('-d', '--disable_email', action='store_true', help='Disable sending email')
args = parser.parse_args()

year_now = dt.datetime.now().year

# Get Firebase data
doc_spot = db.get_document_by_id('forecast_data', LOCAL)
doc_hardcoded = db.get_all_docs_in_collection('hardcoded_jsons')
doc_tide = db.get_document_by_id('tide_stations_data', doc_spot['ref_marinha_tide']).get(f'tide_{year_now}')

# Data forecasts
lat, lon = doc_spot['lat'], doc_spot['lon']
wave_json = stormglass_request(lat, lon, NUMB_DAYS)
tide_json = get_tide_forecasts(doc_tide, doc_hardcoded['tide_specs'], NUMB_DAYS)

t = 0
while (wave_json==None) and (t<3):
    wave_json = stormglass_request(lat, lon, NUMB_DAYS)
    t+=1

if wave_json:
    df_full_forecast = data_to_pandas(wave_json, tide_json, doc_hardcoded, doc_spot['beach_normal_degree'])

    dict_full_forecast, excel_name = save_excel(df_full_forecast)

    db.send_forecast_to_db(LOCAL, dict_full_forecast)
    db.send_history_to_db(LOCAL, dict_full_forecast)

    # if not args.disable_email:
    #     send_email(file_path=f'./{excel_name}', file_name=excel_name)
    # else:
    #     Path(f'./{excel_name}').unlink()
else:
    print('API Request failed.')