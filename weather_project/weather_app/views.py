import datetime
import requests
from django.http import HttpResponse
from django.shortcuts import render
from dotenv import load_dotenv
import os
from utilities.weather_processor import get_weather, get_daily
from .forms import CombinedForm, NewForm
from .models import Rain
from utilities.utils import get_rain_history
import json

load_dotenv()

weather_api_key = os.getenv('weather_api_key')

def index(request):
    form = NewForm()
    if request.method == 'POST':
        city = request.POST['city']
        state = request.POST['state']
          
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
        response2 = requests.get(f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&units=imperial&appid={weather_api_key}')
        weather_data = response2.json()
        daily_weather = get_daily(weather_data)
        first_half, second_half = get_weather(city, weather_data)
        return render(request,'index.html', {'first_half': first_half, 'second_half': second_half, 'form': form, 'daily_weather': daily_weather})
    else:
        return render(request, 'index.html', {'form': form})
       

def history(request):
    if request.method == 'POST':
        city_name = request.POST['city']
        state_name = request.POST['state']
        form = CombinedForm(request.POST)
        dt_begin = None
        dt_end = None
        total_rain: float = 0.0

        if form.is_valid():
            try:
# dt_begin and dt_end are foramtted to be used in the get_rain_history function
                dt_begin = form.cleaned_data['begin_date']
                dt_reset_begin = dt_begin.replace(minute=0, second=0)
                dt_iso_combined_begin = dt_reset_begin.isoformat()
                parsed_date_begin = datetime.datetime.fromisoformat(dt_iso_combined_begin)
                dt_iso_begin = parsed_date_begin.strftime('%Y-%m-%d %H:%M:%S %z UTC')

                dt_end = form.cleaned_data['end_date']
                dt_reset_end = dt_end.replace(minute=0, second=0)
                dt_iso_combined_end = dt_reset_end.isoformat()
                parsed_date_begin = datetime.datetime.fromisoformat(dt_iso_combined_end)
                dt_iso_end = parsed_date_begin.strftime('%Y-%m-%d %H:%M:%S %z UTC')
                print(dt_iso_begin, dt_iso_end, city_name, state_name)

                # get_rain_history is in utils.py and returns a list of dictionaries
                rain_history = get_rain_history(city_name, state_name, dt_iso_begin, dt_iso_end)
                for rain in rain_history:
                   total_rain += rain['one_hour']
                   print(total_rain)
                total_rain = round(total_rain*0.0393701, 2)
            except requests.RequestException as e:
                return HttpResponse(f'Error: {str(e)}')

        return (render(request, 'history.html', {'form': form, 'rain': total_rain}))
    else:
        form = CombinedForm(include_end_date=True)
        return render(request, 'history.html', {'form': form})
    
