import pandas as pd
import folium
from folium.plugins import HeatMap
from flask import Flask,render_template

app = Flask(__name__)

df=pd.read_csv("data.csv")

def createMap(cars):    
    cars.rename(columns={'Lat':'latitude','Long':'longitude'}, inplace=True)
    cars.latitude.fillna(0, inplace = True)
    cars.longitude.fillna(0, inplace = True) 
    CarMap=folium.Map(location=[39,35],zoom_start=6)
    HeatMap(data=cars, radius=16).add_to(CarMap)
    CarMap.save('templates/index.html')
   

@app.route('/<string:Marka>/<string:Model>/')
def index(Marka,Model):
    print(Marka)
    print(Model)
    cars=df[df["Marka"]==Marka].iloc[:,0:2]
    cars=df[df["Model"]==Model].iloc[:,0:2]
    createMap(cars)
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)