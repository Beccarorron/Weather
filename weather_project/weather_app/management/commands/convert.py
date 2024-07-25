from django.core.management.base import BaseCommand
import json
import pandas as pd

class Command(BaseCommand):
    help = 'converts json to dataframe'
    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='The JSON file to load')

    def handle(self, *args, **kwargs):
        json_file_path = kwargs['json_file']

        with open(json_file_path, 'r') as file:
            data = json.load(file,)

        df = pd.json_normalize(data,)
        with open('new_file.csv', 'w') as outfile:
            df.to_csv(outfile,encoding='utf-8')