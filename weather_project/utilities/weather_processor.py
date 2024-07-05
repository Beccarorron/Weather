import datetime

def get_weather(city: str, weather_data):    
    all_weather_data = {
        "City": city,
        # "Date": datetime.datetime.fromtimestamp(weather_data['current']['dt']).strftime('%A'),
        # 'Sunrise': datetime.datetime.fromtimestamp(weather_data['current']['sunrise']).strftime("%I:%M %p"),
        # 'Sunset': datetime.datetime.fromtimestamp(weather_data['current']['sunset']).strftime("%I:%M %p"),
        "Temperature": f"{round(weather_data['current']['temp'], 2)} \u00B0F",
        # "Feels Like": f"{round(weather_data['current']['feels_like'], 2)} \u00B0F",
        # "Humidity": f"{weather_data['current']['humidity']}%",
        "Wind Speed": f"{round(weather_data['current']['wind_speed']*2.237,2)} mph",
        # "Pressure": weather_data['current']['pressure'],
        # "Visibility": f"{round(weather_data['current']['visibility']*.000621,2)} miles",
        # "UVI": weather_data['current']['uvi'],
        "Clouds": f"{weather_data['current']['clouds']} %",
        # "Weather": weather_data['current']['weather'][0]['main'],
        # "Description": weather_data['current']['weather'][0]['description'],
        "Icon": f"https://openweathermap.org/img/wn/{weather_data['current']['weather'][0]['icon']}@2x.png"
        
    }
 
    items = list(all_weather_data.items())
    halfway_point = len(items) // 2
    first_half = dict(items[:halfway_point])
    second_half = dict(items[halfway_point:])

    return first_half, second_half

def get_daily(weather_data):
    if 'daily' in weather_data:  
        processed_data = []
        for day in weather_data['daily']:
            day_info = {
            "Date": datetime.datetime.fromtimestamp(day['dt']).strftime('%A'),
            "Clouds": f"{day['clouds']}%",
                "Rain": f"{day.get('rain', 0)} mm",  # Using .get() to handle cases where 'rain' might not be present
                "Temperature": {
                    "Max": f"{day['temp']['max']} \u00B0F",
                    "Min": f"{day['temp']['min']} \u00B0F"
                },
                "Weather Description": day['weather'][0]['description'],
                "Icon": f"https://openweathermap.org/img/wn/{day['weather'][0]['icon']}@2x.png"
            }
            processed_data.append(day_info)
        for day_info in processed_data:
        # Rename the key
            day_info['Weather_Description'] = day_info.pop('Weather Description')
        return processed_data
          