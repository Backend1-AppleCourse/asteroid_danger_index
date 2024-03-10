

from utilities.file_operations import load, save
from utilities.date_range_generator import generate_date_ranges
from utilities.json_manipulations import filter_response
from utilities.graph_creation import create_graphs, plot_danger_index
import aiohttp 
import asyncio
import json
import matplotlib.pyplot as plt
import numpy as np

class CLI:
    def __init__(self):
        self._api_key = load("secrets.txt")

    def run(self):
        while True:
            options = ["Download NeuWs up to a week", 
            "Download NeuWs for a month", 
            "Present (min_diameter/velocity) graph up to a week", 
            "Present (min_diameter/velocity) graph for a month", 
            "Present (miss_distance/max_diameter) graph up to a week", 
            "Present (miss_distance/max_diameter) graph for a month", 
            "Exit"]
            for index, option in enumerate(options):
                print(f'{index+1}. {option}')
            choosen_option = input(f"Choose an option (1-7):\n")
            while not choosen_option.isdigit() or int(choosen_option) not in range(1, 8):
                choosen_option = input(f"Choose an option: {options}\n")
            choosen = int(choosen_option)

            if choosen == 7:
                break
            elif choosen == 1:
                self.download_neows_up_to_week()
            elif choosen == 2:
                self.download_neows_month()
            elif choosen == 3:
                self.create_graphs_min_diameter_velocity("week",1)
            elif choosen == 4:
                self.create_graphs_min_diameter_velocity("month",1)
            elif choosen == 5:
                self.create_graphs_min_diameter_velocity("week",2)
            elif choosen == 6:
                self.create_graphs_min_diameter_velocity("month",2)

    def download_neows_up_to_week(self):
        json_variable = self._get_neows_up_to_week()
        filename = f'{start_date}_{end_date}_astroids.json'
        save(json_variable, filename)

    def download_neows_month(self):
        combined_month = self._get_neows_month()
        filename = f'{month}_{year}_astroids.json'
        save(combined_month, filename)

    def create_graphs(self, duration_type, request_type):
        if duration_type == "week":
            json_variable = self._get_neows_up_to_week()
            create_graphs(json_variable, request_type)
        elif duration_type == "month":
            json_variable = self._get_neows_month()
            create_graphs(json_variable, request_type)

    def _get_neows_up_to_week(self):
        start_date = input("Enter start date in format yyyy-mm-dd: ")
        end_date = input("Enter end date in format yyyy-mm-dd: ")
        json_variable = filter_response(self._neows_get_request(start_date, end_date, self.api_key))
        return json_variable  

    def _get_neows_month(self):
        month = int(input("Enter month in format mm: "))
        year = int(input("Enter year in format yyyy: "))
        json_variable = self._neows_get_request_month(self.api_key, month, year)
        return json_variable

    def _neows_get_request(start_date, end_date, api_key):
        async def fetch(session, url):
            async with session.get(url) as response:
                return await response.text()
        async def get_response():
            async with aiohttp.ClientSession() as session:
                response = await fetch(session, f'https://api.nasa.gov/neo/rest/v1/feed?start_date={start_date}&end_date={end_date}&api_key={api_key}')
                return response
        return asyncio.run(get_response())

    def _neows_get_request_month(api_key, month, year):
        async def fetch(session, url):
            async with session.get(url) as response:
                return await response.text()

        async def get_responses(api_key, date_ranges):
            async with aiohttp.ClientSession() as session:
                tasks = [
                    fetch(session, f'https://api.nasa.gov/neo/rest/v1/feed?start_date={start_date}&end_date={end_date}&api_key={api_key}')
                    for start_date, end_date in date_ranges
                ]
                return await asyncio.gather(*tasks)

        date_ranges = generate_date_ranges(month, year)
        responses = asyncio.run(get_responses(api_key, date_ranges))

        combined_near_earth_objects = self._combine_near_earth_objects(responses)
        # save(combined_json, "combined")
        first_response = json.loads(responses[0])
        first_response['near_earth_objects'] = json.loads(combined_near_earth_objects)
        combined_month = json.dumps(first_response)
        return combined_month

    def _combine_near_earth_objects(jsons):
        combined_near_earth_objects = {}
        
        for json_object in jsons:
            json_object = filter_response(json_object)
            json_object = json.loads(json_object)
            for date, objects in json_object["near_earth_objects"].items():
                if date in combined_near_earth_objects:
                    combined_near_earth_objects[date].extend(objects)
                else:
                    combined_near_earth_objects[date] = objects
                    
        return json.dumps(combined_near_earth_objects)



