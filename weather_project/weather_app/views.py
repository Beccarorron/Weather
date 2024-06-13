import datetime
import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect
from dotenv import load_dotenv
import os
import json
load_dotenv()

weather_api_key = os.getenv('weather_api_key')

def index(request):
    if request.method == 'POST':
        city = request.POST['city']
        state = request.POST['state']  
        request.session['city'] = city
        try: 
            response = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={city},{state},&appid={weather_api_key}')
            response.raise_for_status()
        except requests.RequestException as e:
            return HttpResponse(f'Error: {str(e)}')

        location_list = response.json()
        if not location_list:
            return HttpResponse('Error: No locations found')
        location_dict = location_list[0]
        lon = round(float(location_dict['lon']), 2) 
        lat = round(float(location_dict['lat']), 2)
        request.session['lat'] = lat
        request.session['lon'] = lon
        return redirect('get_weather')
    else:
        return render(request, 'weather_app/index.html')
       

def get_weather(request):    
    lat = request.session.get('lat')   
    lon = request.session.get('lon')
    city = request.session.get('city')
    response = requests.get(f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely&units=imperial&appid={weather_api_key}')
    weather_data = response.json()
    all_weather_data = {
        "city": city,
        "Date": datetime.datetime.fromtimestamp(weather_data['current']['dt']).strftime('%A'),
        'sunrise': datetime.datetime.fromtimestamp(weather_data['current']['sunrise']).strftime("%I:%M %p"),
        'sunset': datetime.datetime.fromtimestamp(weather_data['current']['sunset']).strftime("%I:%M %p"),
        "temperature": round(weather_data['current']['temp'], 2),
        "feels_like": round(weather_data['current']['feels_like'], 2),
        "humidity": weather_data['current']['humidity'],
        "wind_speed": round(weather_data['current']['wind_speed']*2.237,2),
        "pressure": weather_data['current']['pressure'],
        "visibility": round(weather_data['current']['visibility']*.000621,2),
        "uvi": weather_data['current']['uvi'],
        "clouds": weather_data['current']['clouds'],
        "weather": weather_data['current']['weather'][0]['main'],
        "description": weather_data['current']['weather'][0]['description'],
        "icon": weather_data['current']['weather'][0]['icon']
    }
    
   
    return render(request, 'weather_app/show_weather.html', {'weather_data': all_weather_data,})   
def history(request):
    return render(request, 'weather_app/history.html')

#


