import requests, json 

def codesworth_weather(city_name):
    api_key = "702de1d10db1f8e22c04049b7439455e"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
      
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name 
    response = requests.get(complete_url) 

    x = response.json()

    if x["cod"] != "404":  
        y = x["main"] 
        current_temperature = "{0:.{1}f}".format(y["temp"]-273.15, 2)
        current_pressure = y["pressure"] 
        current_humidity = y["humidity"] 
        z = x["weather"] 
        weather_description = z[0]["description"]
        weather_city = x["name"]
        return (weather_city, current_temperature, current_pressure, current_humidity, weather_description)

    else: 
        return("City not found!")

