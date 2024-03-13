# import sqlite3

# def send_forecast_to_db(df_surf, df_tide):
#     conn = sqlite3.connect('surfsimples.db')
#     cursor = conn.cursor()

#     tide_data = df_tide.values.tolist()
#     tide_data = [(str(row[0]), row[1]) for row in tide_data]
#     cursor.executemany('''INSERT INTO TideForecast (datetime, height)
#                           VALUES (?, ?)''', tide_data)

#     surfing_data = df_surf.values.tolist()
#     surfing_data = [(str(row[0]), *row[1:]) for row in surfing_data]
#     cursor.executemany('''INSERT INTO SurfingForecast (time, 
#                                                        swellDirection_noaa, 
#                                                        swellDirection_sigla, 
#                                                        swellHeight_noaa, 
#                                                        swellPeriod_noaa, 
#                                                        secondarySwellDirection_noaa, 
#                                                        secondarySwellDirection_sigla, 
#                                                        secondarySwellHeight_noaa, 
#                                                        secondarySwellPeriod_noaa, 
#                                                        waveDirection_noaa, 
#                                                        waveDirection_sigla, 
#                                                        waveHeight_noaa, 
#                                                        wavePeriod_noaa, 
#                                                        windDirection_noaa, 
#                                                        windDirection_sigla, 
#                                                        windSpeed_noaa, 
#                                                        windWaveDirection_noaa, 
#                                                        windWaveDirection_sigla, 
#                                                        windWaveHeight_noaa, 
#                                                        windWavePeriod_noaa,
#                                                        wind_direction_class,
#                                                        wind_force_class, 
#                                                        wave_direction_class, 
#                                                        wave_force_class)
#                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', surfing_data)
    
#     conn.commit()
#     conn.close()