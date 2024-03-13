from configs import WIND_DIR_DEGREE, WIND_FOR_KMH, WAVE_DIR_DEGREE, WAVE_FOR_M

beach_norm_angle = 256

def degrees_to_direction(degrees):
    directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    index = round(degrees / (360 / 16)) % 16
    return directions[index]


def classify_wind_dir(wind_angle, beach_normal_angle = beach_norm_angle, wind_dir_data = WIND_DIR_DEGREE):
    wind_angle %= 360
    beach_normal_angle %= 360
    
    angle_diff = abs(wind_angle - beach_normal_angle)
    
    if angle_diff < wind_dir_data['terral']/2 or angle_diff > 360-wind_dir_data['terral']/2:
        return "terral"
    elif angle_diff > 180-wind_dir_data['maral']/2 and angle_diff < 180+wind_dir_data['maral']/2:
        return "maral"
    else:
        return "cruzado"


def classify_wind_for(wind_for, wind_for_data = WIND_FOR_KMH):    
    if wind_for < wind_for_data['liso']:
        return 'liso'
    elif (wind_for >= wind_for_data['liso']) and (wind_for <= wind_for_data['vento_fraco']):
        return 'vento_fraco'
    elif (wind_for >= wind_for_data['vento_fraco']) and (wind_for <= wind_for_data['vento_moderado']):
        return 'vento_moderado'
    elif (wind_for >= wind_for_data['vento_moderado']) and (wind_for <= wind_for_data['vento_forte']):
        return 'vento_forte'
    elif (wind_for >= wind_for_data['vento_forte']) and (wind_for <= wind_for_data['vento_muito_forte']):
        return 'vento_muito_forte'
    else:
        return "vento_extremamente_forte"


def classify_wave_dir(wave_angle, beach_normal_angle = beach_norm_angle, wave_dir_data = WAVE_DIR_DEGREE):
    if beach_normal_angle < 180:
        beach_perpendicular_angle = beach_normal_angle+180
    else:
        beach_perpendicular_angle = beach_normal_angle-180

    wave_angle %= 360
    beach_normal_angle %= 360
    
    angle_diff = wave_angle - beach_perpendicular_angle

    if (angle_diff > -wave_dir_data['reto']) and (angle_diff < wave_dir_data['reto']):
        return 'reto'
    elif (angle_diff >= wave_dir_data['reto']) and (angle_diff < wave_dir_data['reto']+wave_dir_data['inclinado']):
        return 'inclinado_dir'
    elif (angle_diff >= wave_dir_data['reto']+wave_dir_data['inclinado']) and (angle_diff < wave_dir_data['reto']+wave_dir_data['inclinado']+wave_dir_data['muito_inclinado']):
        return 'muito_inclinado_dir'
    elif (angle_diff > -(wave_dir_data['reto']+wave_dir_data['inclinado'])) and (angle_diff <= -wave_dir_data['reto']):
        return 'inclinado_esq'
    elif (angle_diff > -(wave_dir_data['reto']+wave_dir_data['inclinado']+wave_dir_data['muito_inclinado'])) and (angle_diff <= -(wave_dir_data['reto']+wave_dir_data['inclinado'])):
        return 'muito_inclinado_esq'
    else:
        return "sem_ondulacao"


def classify_wave_for(wave_for, wave_for_data = WAVE_FOR_M):    
    if wave_for < wave_for_data['flat']:
        return 'flat'
    elif (wave_for >= wave_for_data['flat']) and (wave_for <= wave_for_data['meio_metrinho']):
        return 'meio_metrinho'
    elif (wave_for >= wave_for_data['meio_metrinho']) and (wave_for <= wave_for_data['meio_metro']):
        return 'meio_metro'
    elif (wave_for >= wave_for_data['meio_metro']) and (wave_for <= wave_for_data['meio_metrao']):
        return 'meio_metrao'
    elif (wave_for >= wave_for_data['meio_metrao']) and (wave_for <= wave_for_data['um_metrinho']):
        return 'um_metrinho'
    elif (wave_for >= wave_for_data['um_metrinho']) and (wave_for <= wave_for_data['um_metrao']):
        return 'um_metrao'
    elif (wave_for >= wave_for_data['um_metrao']) and (wave_for <= wave_for_data['um_metro_e_meio']):
        return 'um_metro_e_meio'
    elif (wave_for >= wave_for_data['um_metro_e_meio']) and (wave_for <= wave_for_data['dois_metros']):
        return 'dois_metros'
    elif (wave_for >= wave_for_data['dois_metros']) and (wave_for <= wave_for_data['tres_metros']):
        return 'tres_metros'
    else:
        return "gigante"