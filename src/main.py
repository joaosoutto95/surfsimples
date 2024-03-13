import argparse

from configs import FIREB_NAME_JSON
from funcs.utils import *
from funcs.tide import *
from classes.Firebase import FirebaseDB


db = FirebaseDB(FIREB_NAME_JSON)

parser = argparse.ArgumentParser(description='Process and send surfing forecast data.')
parser.add_argument('-d', '--disable_email', action='store_true', help='Disable sending email')
args = parser.parse_args()

# Hardcoded Provisorio
local = 'tibau_do_sul_praia_do_amor'
numb_days = 3

# Get Firebase data
doc_spot = db.get_document_by_id('spots_data', local)
doc_hardcoded = db.get_all_docs_in_collection('hardcoded_jsons')
doc_tide = db.get_document_by_id('tide_stations_data', doc_spot['ref_marinha_tide']).get('tide_2024')

# Data forecasts
lat, lon = doc_spot['lat'], doc_spot['lon']
wave_json = stormglass_request(lat, lon, numb_days)
tide_json = get_tide_forecasts(doc_tide, doc_hardcoded['tide_specs'], numb_days)

t = 0
while (wave_json==None) and (t<3):
    wave_json = stormglass_request(lat, lon, numb_days)
    t+=1

if wave_json:
    df_full_forecast = data_to_pandas(wave_json, tide_json)

    dict_full_forecast, excel_name = save_excel(df_full_forecast)

    db.send_forecast_to_db(local, dict_full_forecast)

    # if not args.disable_email:
    #     send_email(file_path=f'./{excel_name}', file_name=excel_name)
    # else:
    #     Path(f'./{excel_name}').unlink()
else:
    print('API Request failed.')

