from flask import Flask, render_template, request
import json
import urllib.request
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/index', methods=['GET', 'POST'])
def index():
    data = {}  # Initialize data dictionary to handle cases when POST is not made or API call fails
    if request.method == 'POST':
        city = request.form['city']
        api_key = os.getenv('OPENWEATHER_API_KEY')
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
        try:
            with urllib.request.urlopen(url) as response:
                list_of_data = json.load(response)
            data = { 
                "country_code": str(list_of_data['sys']['country']), 
                "coordinate": str(list_of_data['coord']['lon']) + ' ' 
                        + str(list_of_data['coord']['lat']), 
                "temp": str(list_of_data['main']['temp']) + '°C', 
                "pressure": str(list_of_data['main']['pressure']), 
                "humidity": str(list_of_data['main']['humidity']), 
            }
            print(data)
        except Exception as e:
            print(f"Error: {e}")
            data['error'] = "Could not retrieve data. Please check the city name or try again later."
    return render_template('index.html', data=data)

    

        

if __name__=='__main__':
    app.run(debug=True)