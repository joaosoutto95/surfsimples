from configs import *
from utils import *

local = NOME_PRAIA + ', ' + ESTADO
data_json = stormglass_request(local)

t = 0
while (data_json==None) and (t<3):
    data_json = stormglass_request(local)
    t+=1

if data_json:
    df_forc, df_tid = data_to_pandas(data_json)

    excel_name = save_excel(df_forc, df_tid)

    send_email(file_path=f'./{excel_name}', file_name=excel_name)

else:
    print('API Request failed.')

