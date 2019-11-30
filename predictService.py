import pandas as pd
df=pd.read_csv("data.csv")
df.drop(columns=['Marka','Lat','Long'],inplace=True)
X=df.iloc[:,0:9].values
y=df.iloc[:,-1].values.reshape(-1, 1) 

from sklearn.preprocessing import LabelEncoder
renkEncoder=LabelEncoder()
renkEncoder.fit(X[:,0])
X[:,0]=renkEncoder.transform(X[:,0])

VitesEncoder=LabelEncoder()
VitesEncoder.fit(X[:,3])
X[:,3]=VitesEncoder.transform(X[:,3])

YakitEncoder=LabelEncoder()
YakitEncoder.fit(X[:,4])
X[:,4]=YakitEncoder.transform(X[:,4])

TipEncoder=LabelEncoder()
TipEncoder.fit(X[:,5])
X[:,5]=TipEncoder.transform(X[:,5])

ItisEncoder=LabelEncoder()
ItisEncoder.fit(X[:,6])
X[:,6]=ItisEncoder.transform(X[:,6])

ModelEncoder=LabelEncoder()
ModelEncoder.fit(X[:,8])
X[:,8]=ModelEncoder.transform(X[:,8])

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
scaler.fit(X)
X=scaler.transform(X)

from sklearn.ensemble import RandomForestRegressor
regressor = RandomForestRegressor(n_estimators=100,random_state = 42)
regressor.fit(X,y)

from flask import Flask
app = Flask(__name__)

import numpy as np
@app.route('/<string:Renk>/<int:KM>/<int:Yil>/<string:Vites>/<string:Yakit>/<string:Tip>/<string:Itis>/<int:Beygir>/<string:Model>')
def index(Renk,KM,Yil,Vites,Yakit,Tip,Itis,Beygir,Model):
    
    Renk=renkEncoder.transform([Renk])
    Vites=VitesEncoder.transform([Vites])
    Yakit=YakitEncoder.transform([Yakit])
    Tip=TipEncoder.transform([Tip])
    Itis=ItisEncoder.transform([Itis])
    Model=ModelEncoder.transform([Model])
    array=np.array([Renk,KM,Yil,Vites,Yakit,Tip,Itis,Beygir,Model]).reshape(1,9)
    request=scaler.transform(array)
    pred=regressor.predict(request)

    return str(pred)

if __name__ == '__main__':
    app.run(debug=True)