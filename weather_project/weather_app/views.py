import datetime
import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect
from dotenv import load_dotenv
import os
from utilities.utils import get_rain
from .forms import DateTimeForm, NewForm
from .models import Rain
from utilities.utils import get_rain_history

load_dotenv()

weather_api_key = os.getenv('weather_api_key')

def index(request):
    form = NewForm()
    if request.method == 'POST':
        city = request.POST['city']
        state = request.POST['state']  
        print(city, state)
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
        return render(request, 'index.html', {'form': form})
       

def get_weather(request):    
    lat = request.session.get('lat')   
    lon = request.session.get('lon')
    city = request.session.get('city')
    response = requests.get(f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely&units=imperial&appid={weather_api_key}')
    weather_data = response.json()
    all_weather_data = {
        "City": city,
        "Date": datetime.datetime.fromtimestamp(weather_data['current']['dt']).strftime('%A'),
        'Sunrise': datetime.datetime.fromtimestamp(weather_data['current']['sunrise']).strftime("%I:%M %p"),
        'Sunset': datetime.datetime.fromtimestamp(weather_data['current']['sunset']).strftime("%I:%M %p"),
        "Temperature": f"{round(weather_data['current']['temp'], 2)} \u00B0F",
        "Feels Like": f"{round(weather_data['current']['feels_like'], 2)} \u00B0F",
        "Humidity": f"{weather_data['current']['humidity']}%",
        "Wind Speed": f"{round(weather_data['current']['wind_speed']*2.237,2)} mph",
        "Pressure": weather_data['current']['pressure'],
        "Visibility": f"{round(weather_data['current']['visibility']*.000621,2)} miles",
        "UVI": weather_data['current']['uvi'],
        "Clouds": f"{weather_data['current']['clouds']} %",
        "Weather": weather_data['current']['weather'][0]['main'],
        "Description": weather_data['current']['weather'][0]['description'],
        "Icon": f"https://openweathermap.org/img/wn/{weather_data['current']['weather'][0]['icon']}@2x.png"
    }
 
    items = list(all_weather_data.items())
    halfway_point = len(items) // 2
    first_half = dict(items[:halfway_point])
    second_half = dict(items[halfway_point:])
    return render(request, 'show_weather.html', {
    'first_half': first_half,
    'second_half': second_half,
    'second_half': second_half,
    })  

def history(request):
    if request.method == 'POST':
        city_name = request.POST['city']
        state_name = request.POST['state']
        form = DateTimeForm(request.POST)
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
        form = DateTimeForm()
        return render(request, 'history.html', {'form': form})
    
from django.shortcuts import render
from .forms import NewForm  # Make sure this import matches the location of your form

def testing(request):
    # Initialize the form variable outside of the if-else scope
    form = NewForm()  # Default form for GET requests
    if request.method == 'POST':  # HTTP methods are uppercase
        print('POST request')
        # Process the form, e.g., form = NewForm(request.POST)
        # Remember to reassign form if you're processing it
    # The form is passed to the template in both GET and POST cases
    return render(request, 'testing.html', {'form': form})