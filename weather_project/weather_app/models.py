from django.db import models


class State(models.Model):
    state = models.CharField(max_length=2, null=True)
    
class City(models.Model):
    lon = models.FloatField()
    lat = models.FloatField()
    city_name = models.CharField(max_length=30)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    
class Time(models.Model):
    city_name = models.ForeignKey(City, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    dt = models.IntegerField()
    dt_iso = models.CharField(max_length=255)
    timezone = models.IntegerField()


class Weather(models.Model):
    city_name = models.ForeignKey(City, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    dt_iso = models.ForeignKey(Time, on_delete=models.CASCADE)
    temp = models.FloatField()
    temp_min = models.FloatField()
    temp_max = models.FloatField()
    feels_like = models.FloatField()
    pressure = models.IntegerField()
    humidity = models.IntegerField()
    dew_point = models.FloatField()

    def __str__(self):
        return f'Weather in {self.city_name.city_name}, {self.state.state} at {self.dt_iso.dt_iso}: {self.temp} degrees'

class Clouds(models.Model):
    city_name = models.ForeignKey(City, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    dt_iso = models.ForeignKey(Time, on_delete=models.CASCADE)
    all = models.IntegerField()

class WeatherDescription(models.Model):
    city_name = models.ForeignKey(City, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    dt_iso = models.ForeignKey(Time, on_delete=models.CASCADE)
    description_id = models.IntegerField(null=True)
    main = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    icon = models.CharField(max_length=255)
    

class Wind(models.Model):
    city_name = models.ForeignKey(City, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    dt_iso = models.ForeignKey(Time, on_delete=models.CASCADE)
    speed = models.FloatField()
    deg = models.IntegerField()

    def __str__(self):
        return f'Wind in {self.city_name.city_name}, {self.state.state} at {self.dt_iso.dt_iso}: {self.speed} m/s {self.deg} degrees'

class Rain(models.Model):
    city_name = models.ForeignKey(City, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    dt_iso = models.ForeignKey(Time, on_delete=models.CASCADE)
    one_hour = models.FloatField(null=True)

    # def __str__(self):
    #     return f'Rain in {self.city_name.city_name}, {self.state.state} at {self.dt_iso.dt_iso}: {self.one_hour}'

class Snow(models.Model):
    city_name = models.ForeignKey(City, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)  
    dt_iso = models.ForeignKey(Time, on_delete=models.CASCADE)
    one_hour = models.FloatField(null=True)

    def __str__(self):
        return f'Snow in {self.city_name.city_name}, {self.state.state} at {self.dt_iso.dt_iso}: {self.one_hour}'
    