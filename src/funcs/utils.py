import time
import unicodedata
import pandas as pd
import datetime as dt
import arrow
import requests

from pathlib import Path
from funcs.email_sender import EmailSender
from funcs.classification import *
from configs import *


def stormglass_request(lat, lon, numb_days=3):
    try:
        start = arrow.now().floor('day').shift(days=-1)
        end = arrow.now().ceil('day').shift(days=numb_days)

        paramit = ','.join(['airTemperature','cloudCover','currentDirection','currentSpeed','gust','humidity','precipitation','waterTemperature',
                            'swellDirection','swellHeight','swellPeriod',
                            'secondarySwellDirection','secondarySwellHeight','secondarySwellPeriod',
                            'waveDirection','waveHeight','wavePeriod',
                            'windWaveDirection','windWaveHeight','windWavePeriod',
                            'windDirection','windSpeed'])

        response = requests.get(
          'https://api.stormglass.io/v2/weather/point',
          params={
            'lat': lat,
            'lng': lon,
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
    except:
        time.sleep(5)
        return None


def data_to_pandas(data_json, tide_dict):
    df_for = pd.DataFrame(pd.json_normalize(data_json['hours']))
    df_tid = pd.DataFrame.from_dict(tide_dict).T.reset_index().rename(columns={'index':'datetime',
                                                                               0:'tide_height',
                                                                               1:'tide_classification'})

    df_for['time'] = pd.to_datetime(df_for['time'])
    df_for = df_for.copy().rename(columns={'time':'datetime'})
    df_tid['datetime'] = pd.to_datetime(df_tid['datetime'])

    selected_hours = ['06:00:00', '09:00:00', '12:00:00', '15:00:00']
    selected_df_for = pd.DataFrame()
    for hour in selected_hours:
        selected_df_for = pd.concat([selected_df_for, df_for[df_for['datetime'].dt.strftime('%H:%M:%S') == hour]])

    df_for = selected_df_for.copy().sort_values('datetime', ascending=True).reset_index(drop=True)
    df_for['datetime'] = df_for['datetime'].dt.tz_localize(None)

    # df_for['datetime'] = df_for['datetime'].dt.tz_convert(BRAZIL_TZ)
    # df_tid['datetime'] = df_tid['datetime'].dt.tz_convert(BRAZIL_TZ)
    
    df_for['swellDirection_sigla'] = df_for['swellDirection.noaa'].apply(degrees_to_direction)
    df_for['secondarySwellDirection_sigla'] = df_for['secondarySwellDirection.noaa'].apply(degrees_to_direction)
    df_for['waveDirection_sigla'] = df_for['waveDirection.noaa'].apply(degrees_to_direction)
    df_for['windDirection_sigla'] = df_for['windDirection.noaa'].apply(degrees_to_direction)
    df_for['windWaveDirection_sigla'] = df_for['windWaveDirection.noaa'].apply(degrees_to_direction)

    df_for['wind_direction_class'] = df_for['windDirection.noaa'].apply(classify_wind_dir)
    df_for['wind_force_class'] = df_for['windSpeed.noaa'].apply(lambda x: classify_wind_for(3.6*x))
    df_for['wave_direction_class'] = df_for['swellDirection.noaa'].apply(classify_wave_dir)
    df_for['wave_force_class'] = df_for['swellHeight.noaa'].apply(classify_wave_for)

    df_for = df_for[['datetime',
                    'swellDirection.noaa', 'swellDirection_sigla', 'swellHeight.noaa', 'swellPeriod.noaa',
                    'secondarySwellDirection.noaa', 'secondarySwellDirection_sigla', 'secondarySwellHeight.noaa', 'secondarySwellPeriod.noaa',
                    'waveDirection.noaa', 'waveDirection_sigla', 'waveHeight.noaa', 'wavePeriod.noaa',
                    'windDirection.noaa', 'windDirection_sigla', 'windSpeed.noaa', 
                    'windWaveDirection.noaa', 'windWaveDirection_sigla', 'windWaveHeight.noaa', 'windWavePeriod.noaa',
                    'wind_direction_class', 'wind_force_class', 'wave_direction_class', 'wave_force_class']].copy()

    df_full = pd.merge(df_for, df_tid, on='datetime', how='left')

    return df_full


def save_excel(df_full_forecast):
    # df_forecast['time'] = df_forecast['time'].apply(lambda x: x.tz_localize(None))
    # df_tides['datetime'] = df_tides['datetime'].apply(lambda x: x.tz_localize(None))

    output_file_name = f'previsao_{dt.datetime.now().strftime("%d_%m_%Y")}.xlsx'
    with pd.ExcelWriter(output_file_name, engine='xlsxwriter') as writer:
        sheets_dataframes = {'previsao': df_full_forecast}

        for sheet_name, df in sheets_dataframes.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)

            worksheet = writer.sheets[sheet_name]

            for i, col in enumerate(df.columns):
                max_len = max(df[col].astype(str).apply(len).max(), len(col))
                worksheet.set_column(i, i, max_len + 2)

    df_full_forecast['datetime'] = df_full_forecast['datetime'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
    dict_full_forecast = df_full_forecast.set_index('datetime').to_dict('index') 

    return dict_full_forecast, output_file_name  


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

        Segue em anexo a planilha dos dados da praia do amor (por enquanto hehe) do dia de ontem ({(dt.datetime.now()-dt.timedelta(days=1)).strftime("%d/%m/%Y")}) até D+3 ({(dt.datetime.now()+dt.timedelta(days=3)).strftime("%d/%m/%Y")}).<br>

        Att.
    """
    sender.send_email(f'Previsao do dia {dt.datetime.now().strftime("%d/%m/%Y")}', html, file_path, attachment_name=file_name)

    Path(file_path).unlink()