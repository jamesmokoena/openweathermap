import requests
import json
from geopy.geocoders import Nominatim
import os
from dotenv import load_dotenv
import os, time
from os.path import exists
import pandas as pd
from IPython import display  
import datetime
from os import path


load_dotenv()


API_KEY = os.getenv('API_KEY')


def path_():
    path = "./Cities"
    return path




def display_():

   
    
    City = input("What is the name of your city? >>> ")

    link = 'https://api.openweathermap.org/data/2.5/weather?q='+City+'&appid='+API_KEY
    json_data = requests.get(link).json()
    

   
    geolocator = Nominatim(user_agent="user_agent")
    location = geolocator.geocode(City)
    
    lat = location.latitude
    lon =location.longitude

    
    file_name = f'{path_()}/{City}-{lat}-{lon}.txt'

    if json_data['cod'] != '404':
        with open(file_name, 'a+') as f:
            json.dump(json_data, f)

        seconds  = time.time() -  os.path.getmtime(file_name)
        minutes = int(seconds) / 60   

        if path.exists(file_name)==True and minutes>180 :
            display()

    else:
        print("Invalid city name, try again")
        display_()


    print("\nDETAILED WEATHER FOR "+City+"\n")
   
    weather = pd.DataFrame(json_data['weather'],index=[0])
    temp =  pd.DataFrame(json_data['main'],index=[1])
    print(weather)
    print('\n',temp)

    
      
display_()   


