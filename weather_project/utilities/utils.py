from django.shortcuts import get_object_or_404
from weather_app.models import City, State, Time, Rain
from datetime import datetime
import pandas as pd
import json
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import seaborn as sns

def get_rain(city_name, state, dt_iso):
    # Get the City, State, and Time objects
    city = get_object_or_404(City, city_name=city_name)
    state = get_object_or_404(State, state=state)
    time = get_object_or_404(Time, dt_iso=dt_iso, city_name=city, state=state)

    # Get the Rain object associated with these objects
    rain = get_object_or_404(Rain, dt_iso=time, city_name=city, state=state)
    return rain


def get_graph():
    graph=''
    sns.set_theme()
    sns.color_palette("magma", as_cmap=True)
    buffer = BytesIO()
    plt.savefig(buffer, format=('png'))
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_plot(x,y,condition):
    
    plt.switch_backend("AGG")
    # plt.style.use('seaborn')
    plt.figure(figsize=(7,4))
    print(x,y)
    # plt.plot_date(x,y,linestyle='solid')
    plt.title(f'North Bend {condition} Totals by day')
    plt.gcf().autofmt_xdate()
    plt.bar(x,y)
    # plt.plot(x,y)
    plt.xticks(rotation=45)
    plt.xlabel('dates')
    plt.ylabel(f'inches of {condition}')
    plt.tight_layout()
    graph = get_graph()
    return graph
