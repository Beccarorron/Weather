from django.core.management.base import BaseCommand
from weather_app.models import Weather, Clouds, WeatherDescription, Wind, City, Time, Rain, Snow, State
import json
class Command(BaseCommand):
    help = 'Loads a JSON file into the database'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='The JSON file to load')

    def handle(self, *args, **kwargs):
        json_file_path = kwargs['json_file']
        with open(json_file_path, 'r') as file:
            data = json.load(file)
            state, _ = State.objects.get_or_create(state='OR')
            for city_data in data:
                city, _ = City.objects.get_or_create(
                    lon=city_data['lon'],
                    lat=city_data['lat'],
                    city_name=city_data['city_name'],
                    state=state
                )
                time = Time.objects.create(
                    dt=city_data['dt'],
                    dt_iso=city_data['dt_iso'],
                    timezone=city_data['timezone'],
                    city_name=city,
                    state=state
                )
                weather = Weather.objects.create(
                    city_name=city,
                    state=state,
                    dt_iso=time,
                    temp=city_data['main']['temp'],
                    temp_min=city_data['main']['temp_min'],
                    temp_max=city_data['main']['temp_max'],
                    feels_like=city_data['main']['feels_like'],
                    pressure=city_data['main']['pressure'],
                    humidity=city_data['main']['humidity'],
                    dew_point=city_data['main']['dew_point']
                )
                Clouds.objects.create(
                    city_name=city,
                    state = state,  
                    dt_iso=time,
                    all=city_data['clouds']['all']
                )
                for description in city_data['weather']:
                    WeatherDescription.objects.create(
                        city_name=city,
                        state=state,
                        dt_iso=time,
                        description_id=description['id'],
                        main=description['main'],
                        description=description['description'],
                        icon=description['icon']
                    )
                Wind.objects.create(
                    city_name=city,
                    state=state,
                    dt_iso=time,
                    speed=city_data['wind']['speed'],
                    deg=city_data['wind']['deg']
                )
                if 'rain' in city_data:
                    Rain.objects.create(
                        city_name=city,
                        state=state,
                        dt_iso=time,
                        one_hour=city_data['rain']['1h']
                        )
                if 'snow' in city_data:
                    Snow.objects.create(
                        city_name=city,
                        state=state,
                        dt_iso=time,
                        one_hour=city_data['snow']['1h']
                    )
                