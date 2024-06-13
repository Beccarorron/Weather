from django.core.management.base import BaseCommand, CommandError
from django.shortcuts import get_object_or_404
from weather_app.models import City, State, Time, Rain

class Command(BaseCommand):
    help = 'Description of your command'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--city',
            dest='city',
            help='City name',
        )

        parser.add_argument(
            '--state',
            dest='state',
            help='State name',
        )

        parser.add_argument(
            '--dt_iso',
            dest='dt_iso',
            help='Datetime in ISO format',
        )

    def handle(self, *args, **options):
        city_name = options['city']
        state_name = options['state']
        dt_iso_string = options['dt_iso']

        try:
            rain = self.get_rain(city_name, state_name, dt_iso_string)
            self.stdout.write(self.style.SUCCESS(f'Successfully got rain object {rain}'))
        except Exception as e:
            raise CommandError(f'Error occurred: {str(e)}')

    def get_rain(self, city_name, state_name, dt_iso_string):
        # Get the City, State, and Time objects
        city = get_object_or_404(City, city_name=city_name)
        state = get_object_or_404(State, state=state_name)
        time = get_object_or_404(Time, dt_iso=dt_iso_string, city_name=city, state=state)

        # Get the Rain object associated with these objects
        rain = get_object_or_404(Rain, dt_iso=time, city_name=city, state=state)

        return rain