from django.contrib import admin
from .models import City, Time, Weather, Clouds, WeatherDescription, Wind, Rain, Snow, State

admin.site.register(City)
admin.site.register(State)
admin.site.register(Time)
admin.site.register(Weather)
admin.site.register(Clouds)
admin.site.register(WeatherDescription)
admin.site.register(Wind)
admin.site.register(Rain)
admin.site.register(Snow)



