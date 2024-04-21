def degrees_to_direction(degrees):
    directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSO', 'SO', 'OSO', 'O', 'ONO', 'NO', 'NNO']
    index = round(degrees / (360 / 16)) % 16
    return directions[index]


def classify_wind_dir(wind_angle, beach_normal_angle, wind_dir_data):
    wind_angle %= 360
    beach_normal_angle %= 360
    
    angle_diff = abs(wind_angle - beach_normal_angle)
    
    if angle_diff < wind_dir_data['terral']/2 or angle_diff > 360-wind_dir_data['terral']/2:
        return "Terral"
    elif angle_diff > 180-wind_dir_data['maral']/2 and angle_diff < 180+wind_dir_data['maral']/2:
        return "Maral"
    else:
        return "Cruzado"


def classify_wind_for(wind_for, wind_for_data):    
    if wind_for < wind_for_data['liso']:
        return 'liso'
    elif (wind_for >= wind_for_data['liso']) and (wind_for <= wind_for_data['vento_fraco']):
        return 'fraco'
    elif (wind_for >= wind_for_data['vento_fraco']) and (wind_for <= wind_for_data['vento_moderado']):
        return 'moderado'
    elif (wind_for >= wind_for_data['vento_moderado']) and (wind_for <= wind_for_data['vento_forte']):
        return 'forte'
    elif (wind_for >= wind_for_data['vento_forte']) and (wind_for <= wind_for_data['vento_muito_forte']):
        return 'muito forte'
    else:
        return 'muito forte'


def classify_wave_dir(wave_angle, beach_normal_angle, wave_dir_data):
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
        return 'inclinado'
    elif (angle_diff >= wave_dir_data['reto']+wave_dir_data['inclinado']) and (angle_diff < wave_dir_data['reto']+wave_dir_data['inclinado']+wave_dir_data['muito_inclinado']):
        return 'muito inclinado'
    elif (angle_diff > -(wave_dir_data['reto']+wave_dir_data['inclinado'])) and (angle_diff <= -wave_dir_data['reto']):
        return 'inclinado'
    elif (angle_diff > -(wave_dir_data['reto']+wave_dir_data['inclinado']+wave_dir_data['muito_inclinado'])) and (angle_diff <= -(wave_dir_data['reto']+wave_dir_data['inclinado'])):
        return 'muito inclinado'
    else:
        return "sem onda"


def classify_wave_for(wave_for, wave_for_data):    
    if wave_for < wave_for_data['flat']:
        return 'Flat'
    elif (wave_for >= wave_for_data['flat']) and (wave_for <= wave_for_data['meio_metrinho']):
        return 'Meio metrinho'
    elif (wave_for >= wave_for_data['meio_metrinho']) and (wave_for <= wave_for_data['meio_metro']):
        return 'Meio metro'
    elif (wave_for >= wave_for_data['meio_metro']) and (wave_for <= wave_for_data['meio_metrao']):
        return 'Meio metrão'
    elif (wave_for >= wave_for_data['meio_metrao']) and (wave_for <= wave_for_data['um_metrinho']):
        return 'Um metrinho'
    elif (wave_for >= wave_for_data['um_metrinho']) and (wave_for <= wave_for_data['um_metrao']):
        return 'Um metrão'
    elif (wave_for >= wave_for_data['um_metrao']) and (wave_for <= wave_for_data['um_metro_e_meio']):
        return 'Um metro e meio'
    elif (wave_for >= wave_for_data['um_metro_e_meio']) and (wave_for <= wave_for_data['dois_metros']):
        return 'Dois metros'
    elif (wave_for >= wave_for_data['dois_metros']) and (wave_for <= wave_for_data['tres_metros']):
        return 'Três metros'
    else:
        return "Gigante"
    

def classify_combination(combinations, VD, VF, OD, OF):
    for combination in combinations:
        if (combination['VD'] == VD and
            combination['VF'] == VF and
            combination['OD'] == OD and
            combination['OF'] == OF):
            return combination['resultado']