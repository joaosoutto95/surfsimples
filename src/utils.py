import unicodedata
import pandas as pd
import datetime as dt
import arrow
import requests
import urllib.parse

from pathlib import Path
from email_sender import *
from configs import *

def stormglass_request(local):
    url = f'https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(local)}`&format=jsonv2'

    response = requests.get(url).json()

    latitude = response[0]["lat"]
    longitude = response[0]["lon"]

    start = arrow.now().floor('day').shift(days=-1)
    end = arrow.now().ceil('day').shift(days=1)

    paramit = ','.join(['airTemperature','cloudCover','currentDirection','currentSpeed','gust','humidity','precipitation','waterTemperature',
                        'swellDirection','swellHeight','swellPeriod',
                        'secondarySwellDirection','secondarySwellHeight','secondarySwellPeriod',
                        'waveDirection','waveHeight','wavePeriod',
                        'windWaveDirection','windWaveHeight','windWavePeriod',
                        'windDirection','windSpeed'])

    response = requests.get(
      'https://api.stormglass.io/v2/weather/point',
      params={
        'lat': latitude,
        'lng': longitude,
        'params': paramit,
        'start': start.to('UTC').timestamp(),
        'end': end.to('UTC').timestamp() 
      },
      headers={
        'Authorization': API_KEY
      }
    )

    json_data = response.json()
    return json_data

def degrees_to_direction(degrees):
    directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    index = round(degrees / (360 / 16)) % 16
    return directions[index]

def data_to_pandas(data_json):
    df_for = pd.DataFrame(pd.json_normalize(data_json['hours']))
    df_tid = pd.read_csv('mare_natal.csv')

    df_for['time'] = pd.to_datetime(df_for['time'])
    df_tid['datetime'] = pd.to_datetime(df_tid['datetime'])

    df_for['time'] = df_for['time'].dt.tz_convert(BRAZIL_TZ)
    df_tid['datetime'] = df_tid['datetime'].dt.tz_convert(BRAZIL_TZ)

    df_for['swellDirection_sigla'] = df_for['swellDirection.noaa'].apply(degrees_to_direction)
    df_for['secondarySwellDirection_sigla'] = df_for['secondarySwellDirection.noaa'].apply(degrees_to_direction)
    df_for['waveDirection_sigla'] = df_for['waveDirection.noaa'].apply(degrees_to_direction)
    df_for['windDirection_sigla'] = df_for['windDirection.noaa'].apply(degrees_to_direction)
    df_for['windWaveDirection_sigla'] = df_for['windWaveDirection.noaa'].apply(degrees_to_direction)

    df_for = df_for[['time',
                    'swellDirection.noaa', 'swellDirection_sigla', 'swellHeight.noaa', 'swellPeriod.noaa',
                    'secondarySwellDirection.noaa', 'secondarySwellDirection_sigla', 'secondarySwellHeight.noaa', 'secondarySwellPeriod.noaa',
                    'waveDirection.noaa', 'waveDirection_sigla', 'waveHeight.noaa', 'wavePeriod.noaa',
                    'windDirection.noaa', 'windDirection_sigla', 'windSpeed.noaa', 
                    'windWaveDirection.noaa', 'windWaveDirection_sigla', 'windWaveHeight.noaa', 'windWavePeriod.noaa']].copy()

    df_tide_3days = df_tid[(df_tid['datetime']>=df_for['time'][0])&
                           (df_tid['datetime']<(df_for['time'][0]+dt.timedelta(days=3)).replace(hour=0, minute=0, second=0, microsecond=0))].copy().reset_index(drop=True)
    
    return df_for, df_tide_3days

def save_excel(df_forecast, df_tides):
    df_forecast['time'] = df_forecast['time'].apply(lambda x: x.tz_localize(None))
    df_tides['datetime'] = df_tides['datetime'].apply(lambda x: x.tz_localize(None))

    output_file_name = f'previsao_{dt.datetime.now().strftime("%d_%m_%Y")}.xlsx'
    with pd.ExcelWriter(output_file_name, engine='xlsxwriter') as writer:
        sheets_dataframes = {'previsao': df_forecast, 'mare': df_tides}

        for sheet_name, df in sheets_dataframes.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)

            worksheet = writer.sheets[sheet_name]

            for i, col in enumerate(df.columns):
                max_len = max(df[col].astype(str).apply(len).max(), len(col))
                worksheet.set_column(i, i, max_len + 2)

    return output_file_name  

def to_snake_case(name):
    name = name.replace(' ', '_')
    name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')
    name = ''.join(e for e in name if e.isalnum() or e == '_')
    name = name.lower()
    return name

def send_email(file_path=None, file_name=None):
    print('Enviando email')

    sender = EmailSender(EMAIL_SENDER, EMAIL_PASSWORD)
    html = f"""
        Coe Thadeuzao,<br>

        Segue em anexo a planilha dos dados da praia do amor (por enquanto hehe) do dia de ontem ({(dt.datetime.now()-dt.timedelta(days=1)).strftime("%d/%m/%Y")}) até amanhã ({(dt.datetime.now()+dt.timedelta(days=1)).strftime("%d/%m/%Y")}).<br>

        Att.
    """
    sender.send_email(f'Previsao do dia {dt.datetime.now().strftime("%d/%m/%Y")}', html, file_path, attachment_name=file_name)

    Path(file_path).unlink()