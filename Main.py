import requests
import json
from geopy.geocoders import Nominatim
import os
from dotenv import load_dotenv
import os, time
import pandas as pd


load_dotenv()


API_KEY = os.getenv('API_KEY')


def path_():
    path = "./Cities"
    return path

def get_city():
    City = input("What is the name of your city? >>> ")
    return City




def api_request(city):
    link = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid='+API_KEY
    json_data = requests.get(link).json()

    return json_data    



def forecast(json_data):       

    weather = json_data['weather']
    temp =  json_data['main']

    return weather,temp



def convert_city_to_coordinates(city):

    geolocator = Nominatim(user_agent="user_agent")
    location = geolocator.geocode(city)
    
    lat = location.latitude
    lon =location.longitude
    return lat, lon



def latest_weather(lat,lon):
    link = f"https://pro.openweathermap.org/data/2.5/forecast/hourly?lat={lat}&lon={lon}&appid={API_key}"
    json_data = requests.get(link).json()
    hourly_data = {"Temp": json_data[0]["main"]["temp"], "Description": json_data[0]["weather"],"Time": json_data[0]["dt_txt"]}
    return hourly_data


def create_file(city,json_data,lat,lon):

    file_name = f'{path_()}/{city}-{lat}-{lon}.txt'
    with open(file_name, 'a+') as f:
        json.dump(json_data, f)
    return file_name    





def old_file(file_name):
    seconds  = time.time() -  os.path.getmtime(file_name)
    minutes = int(seconds) / 60  

    if os.path.exists(file_name) and minutes >180 :
        return False
   


def app():
    
    city = get_city() 

    
    json_data= api_request(city)

    while json_data['cod'] == '404':
        city = get_city()

        

    weather, temp= forecast(json_data)
    lat,lon = convert_city_to_coordinates(city)
    
    file = create_file(city,json_data,lat,lon)
        
        

    if old_file(file):
        city = get_city() 
        lat,lon = convert_city_to_coordinates(city)
        new_forecast = latest_weather(lat,lon)
       

        new_weather = pd.DataFrame(new_forecast['weather'],index=[0])
        new_temp =  pd.DataFrame(new_forecast['main'],index=[1])

        print("______________________________________________________")
        print(new_weather)
        print("______________________________________________________")
        print(new_temp)
       
    
    weather = pd.DataFrame(json_data['weather'],index=[0])
    temp =  pd.DataFrame(json_data['main'],index=[1])
    print("______________________________________________________")
    print(weather)
    print("______________________________________________________")
    print(temp)    



if __name__ == '__main__':
    app()





    


    


   





    

    

        





    





    
    



    


    











  


