from flask import Flask,render_template,request
from urllib.parse import quote
from urllib.request import urlopen
import json
import requests


app = Flask(__name__)

OPEN_WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={0}&units=metric&APPID={1}"

OPEN_WEATHER_KEY = '90cf35a3566e06ec100fa7d37db635a9'

NEWS_URL = "http://newsapi.org/v2/everything?q={0}&from=2021-1-30&sortBy=publishedAt&apiKey={1}"

NEWS_KEY = "5b40f454fee1460db33f6d165a7350c0"


url = requests.get('https://covid19.th-stat.com/api/open/today')
r = url.json()
Confirmed = r['Confirmed']
Recovered = r['Recovered']
Hospitalized = r['Hospitalized']
Deaths = r['Deaths']
result = {
    'Confirmed' : Confirmed,
    'Recovered' : Recovered,
    'Hospitalized' : Hospitalized,
    'Deaths' : Deaths


}

@app.route("/")
def home():
    city = request.args.get('city')
    if not city:
        city = 'Bangkok'
   
    weather = get_weather(city, OPEN_WEATHER_KEY)
    news = CovidNews()

    return render_template("home.html", weather=weather,result=result,news=news)

def CovidNews():
    url = "http://newsapi.org/v2/everything?q=tesla&from=2021-01-01&sortBy=publishedAt&apiKey=5b40f454fee1460db33f6d165a7350c0"
    data = urlopen(url).read()
    parsed = json.loads(data)
    news = []
    
    for i in range(0,5): #แก้ให้เริ่มที่ 1
        title = parsed['articles'][i]['title']
        description = parsed['articles'][i]['description']
        img = parsed['articles'][i]['urlToImage']
        link = parsed['articles'][i]['url']
        news.append({"title":title,"description":description,"Link":link,"img":img})
        
    return news
    

def get_weather(city,API_KEY):
    query = quote(city)
    url = OPEN_WEATHER_URL.format(city, API_KEY)
    data = urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    
    if parsed.get('weather'):

        description = parsed['weather'][0]['description']
        temperature = parsed['main']['temp']
        pressure = parsed['main']['pressure']
        humidity = parsed['main']['humidity']
        wind = parsed['wind']['speed']
        city = parsed['name']
        country = parsed['sys']['country']
        icon = parsed['weather'][0]['icon']
        url = 'http://openweathermap.org/img/wn/{icon}.png'.format(icon=icon)
        weather = {'description': description,
                   'temperature': temperature,
                   'city': city,
                   'country': country,
                   'icon' : icon,
                   'pressure' : pressure ,
                   'humidity' : humidity ,
                   'wind' : wind ,
                   'url' : url
                   
                   }
      
    return weather

@app.route('/news')
def news():
    word = request.args.get('word')
    if not word:
        word = 'covid'
   
    news = get_news(word, NEWS_KEY)
    return render_template('news.html',news=news)

def get_news(word,NEWS_KEY):
    query = quote(word)
    url = NEWS_URL.format(word, NEWS_KEY)
    data = urlopen(url).read()
    parsed = json.loads(data)
    news = []
    
    for i in range(len(parsed['articles'])):
        title = parsed['articles'][i]['title']
        description = parsed['articles'][i]['description']
        img = parsed['articles'][i]['urlToImage']
        link = parsed['articles'][i]['url']
        news.append({"title":title,"description":description,"Link":link,"img":img})
    
    return news

    


@app.route('/about')
def about():
   return render_template('about.html')

app.run(debug=True,use_reloader=True)