import datetime
import requests
from django.http import HttpResponse
from django.shortcuts import render
from dotenv import load_dotenv
import os
import pandas as pd
from .forms import CombinedForm, NewForm
from .models import Rain, Snow
from utilities.weather_processor import get_daily, get_weather
import numpy as np
from utilities.utils import get_plot

import csv

# import urllib
# import matplotlib.pyplot as plt
# import io, base64
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
        city = request.POST['city']
        state_name = request.POST['state']
        form = CombinedForm(request.POST)
        dt_begin = None
        dt_end = None

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
                print(dt_iso_begin, dt_iso_end, city, state_name)
                
                new_query  = list(Rain.objects.filter(dt_iso__dt_iso__range=(dt_iso_begin, dt_iso_end),city_name__city_name=city,state__state=state_name).values_list('city_name__city_name','state__state','dt_iso__dt_iso','one_hour'))
                df = pd.DataFrame(new_query, columns=['city','state','dates','rain'])
                df['dates'] = df['dates'].str.slice(0,16)
                df['dates'] = pd.to_datetime(df['dates'], format='%Y-%m-%d %H:%M')
                df.to_csv('rain.csv', encoding='utf-8')

                rain_axis:list =  df['rain'].groupby(df['dates'].dt.to_period('D')).sum().mul(.0393701)
                date_axis:list = rain_axis.axes
                
                for date in date_axis:
                    df = pd.Series(date,index=date).astype(dtype='datetime64[ns]')                        
                    
                x = [x for x in df]
                y = [y for y in rain_axis]
                condition:str = 'rain'
                graph = get_plot(x,y,condition)
            except requests.RequestException as e:
                return HttpResponse(f'Error: {str(e)}')
        return (render(request, 'history.html', {'form':form,'chart': graph}))
    else:
        form = CombinedForm(include_end_date=True)
        return render(request, 'history.html', {'form': form})
    
 
def get_snow(request):
    if request.method == 'POST':
        city = request.POST['city']
        state_name = request.POST['state']
        form = CombinedForm(request.POST)
        dt_begin = None
        dt_end = None

        if form.is_valid():
            try:
# dt_begin and dt_end are foramtted to be used in the snow.objests query
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
                print(dt_iso_begin, dt_iso_end, city, state_name)
                
                new_query  = list(Snow.objects.filter(dt_iso__dt_iso__range=(dt_iso_begin, dt_iso_end),city_name__city_name=city,state__state=state_name).values_list('city_name__city_name','state__state','dt_iso__dt_iso','one_hour'))
                df = pd.DataFrame(new_query, columns=['city','state','dates','snow'])
                df['dates'] = df['dates'].str.slice(0,16)
                df['dates'] = pd.to_datetime(df['dates'], format='%Y-%m-%d %H:%M')
                df.to_csv('snow.csv', encoding='utf-8')

                snow_axis:list =  df['snow'].groupby(df['dates'].dt.to_period('D')).sum().mul(.0393701)
                date_axis:list = snow_axis.axes
                
                for date in date_axis:
                    df = pd.Series(date,index=date).astype(dtype='datetime64[ns]')                        
                    
                x = [x for x in df]
                y = [y for y in snow_axis]
                condition ='snow'
                graph = get_plot(x,y,condition)
            except requests.RequestException as e:
                return HttpResponse(f'Error: {str(e)}')
        return (render(request, 'snow.html', {'form':form,'chart': graph}))
    else:
        form = CombinedForm(include_end_date=True)
        return render(request, 'snow.html', {'form': form})   