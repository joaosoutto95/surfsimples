from datetime import datetime, timedelta

def filter_dictionary_for_day(dict_tide, list_dates_str):
    dates = [datetime.strptime(date_str, '%Y-%m-%d').date() for date_str in list_dates_str]
    dates.insert(0, (datetime.strptime(list_dates_str[0], '%Y-%m-%d') - timedelta(days=1)).date())
    dates.insert(-1, (datetime.strptime(list_dates_str[-1], '%Y-%m-%d') + timedelta(days=1)).date())
    
    filtered_dict = {}
    for date in dates:
        for key, value in dict_tide.items():
            datetime_key = datetime.strptime(key, '%Y-%m-%d %H:%M:%S')
            if datetime_key.date() == date:
                filtered_dict[key] = value

    return filtered_dict


def interpolate_tides(tide_data, dates, tide_hardcoded):
    interpolated_values = {}

    date_list = []
    for date in dates:
        target_hours = [f'{date} 03:00:00', f'{date} 06:00:00', f'{date} 09:00:00', f'{date} 12:00:00', f'{date} 15:00:00', f'{date} 18:00:00']
        date_list = date_list + target_hours

    for target_hour in date_list:
        target_time = datetime.strptime(target_hour, '%Y-%m-%d %H:%M:%S')
        last_before = None
        for key, value in sorted(tide_data.items()):
            tide_time = datetime.strptime(key, '%Y-%m-%d %H:%M:%S')
            if tide_time < target_time:
                last_before = (tide_time, value)
            else:
                break

        right_after = None
        for key, value in sorted(tide_data.items()):
            tide_time = datetime.strptime(key, '%Y-%m-%d %H:%M:%S')
            if tide_time > target_time:
                right_after = (tide_time, value)
                break    
        
        interpolated_value = round(last_before[1] + (target_time - last_before[0]) / (right_after[0] - last_before[0]) * (right_after[1] - last_before[1]), 1)
        if right_after[1] - last_before[1] > tide_hardcoded['mare_morta']:
            percent = (interpolated_value - last_before[1])/(right_after[1] - last_before[1])
            if interpolated_value==last_before[1]:
                class_tide = 'mare baixa'
                interpolated_values[target_hour] = (interpolated_value, class_tide)
                continue

            if interpolated_value==right_after[1]:
                class_tide = 'mare alta'
                interpolated_values[target_hour] = (interpolated_value, class_tide)
                continue

            if percent <= tide_hardcoded['mare_baixa']:
                class_tide = 'mare baixa subindo'
            elif percent >= tide_hardcoded['mare_baixa']+tide_hardcoded['meia_mare']:
                class_tide = 'mare alta subindo'
            else:
                class_tide = 'meia mare subindo'

        elif ((right_after[1] - last_before[1]) <= tide_hardcoded['mare_morta']) and (right_after[1] - last_before[1]) >= -tide_hardcoded['mare_morta']:
            class_tide = 'mare morta'

        else:
            percent = (interpolated_value - last_before[1])/(right_after[1] - last_before[1])
            if interpolated_value==last_before[1]:
                class_tide = 'mare alta'
                interpolated_values[target_hour] = (interpolated_value, class_tide)
                continue

            if interpolated_value==right_after[1]:
                class_tide = 'mare baixa'
                interpolated_values[target_hour] = (interpolated_value, class_tide)
                continue

            if percent <= tide_hardcoded['mare_alta']:
                class_tide = 'mare alta descendo'
            elif percent >= tide_hardcoded['mare_alta']+tide_hardcoded['meia_mare']:
                class_tide = 'mare baixa descendo'
            else:
                class_tide = 'meia mare descendo'

        interpolated_values[target_hour] = (interpolated_value, class_tide)
        
    return interpolated_values


def get_tide_forecasts(tide_data, tide_definition, numb_days=3):
    date_list = [(datetime.now().date() - timedelta(days=1)).strftime('%Y-%m-%d')]
    for i in range(numb_days+1):
        date_list.append((datetime.now().date() + timedelta(days=i)).strftime('%Y-%m-%d'))
    
    filtered_tide_times_dict = filter_dictionary_for_day(tide_data, date_list)
    interpolated_values = interpolate_tides(filtered_tide_times_dict, date_list, tide_definition)
    
    return interpolated_values 