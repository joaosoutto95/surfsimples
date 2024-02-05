from datetime import datetime, timedelta
from configs import *
from utils import *

# folder_name = os.path.split(os.getcwd())[-1]
# df_for = pd.read_csv('prev_2024-02-04.csv')

local = NOME_PRAIA + ', ' + ESTADO
data_json = stormglass_request(local)

df_forc, df_tid = data_to_pandas(data_json)

excel_name = save_excel(df_forc, df_tid)

send_email(file_path=f'./{excel_name}', file_name=excel_name)

