import argparse

from configs import *
from utils import *
from manage_db import *

parser = argparse.ArgumentParser(description='Process and send surfing forecast data.')
parser.add_argument('-d', '--disable_email', action='store_true', help='Disable sending email')
args = parser.parse_args()

local = NOME_PRAIA + ', ' + ESTADO
data_json = stormglass_request(local)

t = 0
while (data_json==None) and (t<3):
    data_json = stormglass_request(local)
    t+=1

if data_json:
    df_forc, df_tid = data_to_pandas(data_json)

    df_forc_1day, df_tides_1day, excel_name = save_excel(df_forc, df_tid)

    send_forecast_to_db(df_forc_1day, df_tides_1day)
    if not args.disable_email:
        send_email(file_path=f'./{excel_name}', file_name=excel_name)
    else:
        Path(f'./{excel_name}').unlink()
else:
    print('API Request failed.')

