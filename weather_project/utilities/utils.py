from django.shortcuts import get_object_or_404
from weather_app.models import City, State, Time, Rain


def get_rain(city_name, state, dt_iso):
	# Get the City, State, and Time objects
	city = get_object_or_404(City, city_name=city_name)
	state = get_object_or_404(State, state=state)
	time = get_object_or_404(Time, dt_iso=dt_iso, city_name=city, state=state)

	# Get the Rain object associated with these objects
	rain = get_object_or_404(Rain, dt_iso=time, city_name=city, state=state)
	return rain

def get_rain_history(city_name, state_name, dt_iso_begin, dt_iso_end):
    # Get the City and State objects
    city_name = get_object_or_404(City, city_name=city_name)
    state = get_object_or_404(State, state=state_name)
    time_objects = Time.objects.filter(dt_iso__range=(dt_iso_begin, dt_iso_end), city_name=city_name, state=state)
    # Get the Time objects
    
    # Get the Rain objects associated with these Time objects
    rain_history_data = Rain.objects.filter(dt_iso__in=time_objects, city_name=city_name, state=state)
    rain_history_list = list(rain_history_data.values())

    return rain_history_list