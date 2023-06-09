import requests
import json
from geopy.geocoders import Nominatim
import os
from dotenv import load_dotenv
import os, time
import pandas as pd


load_dotenv()


API_KEY = os.getenv('api_key')


def get_api_key():
    api_key = input("Enter your API key >>> ")
    return api_key



def save_api_key(api_key):
    with open(".env", "w") as f:
        f.write(f"AP_KEY= {api_key}")
    



def path_():
    path = "./Cities"
    return path

def get_city(api_key):
    city = ""
    while True:
        city = input("What is the name of your city? >>> ")
        json_data = api_request(api_key,city)

        if json_data['cod'] == '404':
            print("Invalid city, please try again\n")
            continue
        else:
            break

    return city




def api_request(api_key,city):
    link = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid='+api_key
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



def latest_weather(api_key,lat,lon):
    link = f"https://pro.openweathermap.org/data/2.5/forecast/hourly?lat={lat}&lon={lon}&appid={api_key}"
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
    
    api_key = get_api_key()

    save_api_key(api_key)

    city = get_city(api_key) 
    json_data= api_request(api_key,city)

    weather, temp= forecast(json_data)
    lat,lon = convert_city_to_coordinates(city)
    
    file = create_file(city,json_data,lat,lon)
            
            

    if old_file(file):
        city = get_city(api_key) 
        lat,lon = convert_city_to_coordinates(city)
        new_forecast = latest_weather(api_key,lat,lon)
    

        new_weather = pd.DataFrame(new_forecast['weather'],index=[0])
        new_temp =  pd.DataFrame(new_forecast['main'],index=[1])

        print("______________________________________________________\n")
        print(new_weather)
        print("______________________________________________________\n")
        print(new_temp)
    
    
    weather = pd.DataFrame(json_data['weather'],index=[0])
    temp =  pd.DataFrame(json_data['main'],index=[1])
    print("______________________________________________________\n")
    print(weather)
    print("______________________________________________________\n")
    print(temp)    



if __name__ == '__main__':
    app()





    


    


   





    

    

        





    





    
    



    


    











  


