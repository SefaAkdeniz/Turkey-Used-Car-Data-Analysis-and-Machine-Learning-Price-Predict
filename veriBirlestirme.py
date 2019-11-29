import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog

Response=pd.read_json("1.json",encoding="UTF-8")                        
carList=Response["response"]["classifieds"]
df=pd.DataFrame(carList)

for each in range(2,295):
    try:
        Response=pd.read_json(str(each)+".json",encoding="UTF-8")                        
        carList=Response["response"]["classifieds"]
        df2=pd.DataFrame(carList)
        print(str(int((each/294)*100)))
        df=np.concatenate((df, df2), axis=0)
        df=pd.DataFrame(df)
    except:
        try:
            Response=pd.read_json(str(each)+".json",encoding="ANSI")                        
            carList=Response["response"]["classifieds"]
            df2=pd.DataFrame(carList)
            print(str(int((each/294)*100)))       
            df=np.concatenate((df, df2), axis=0)
            df=pd.DataFrame(df)
        except:
            print("HATA: "+str(each))

df.columns=[each for each in df2.columns]

new_columns=dict(df.attributes)
new_columns=new_columns[0]
new_columns=list(new_columns.keys())
for each in new_columns:
    try:
        df[each]=[dict(index)[each] for index in df.attributes]
    except:
        pass

new_columns2=dict(df.categoryBreadcrumb)
new_columns2=new_columns2[0]
new_columns2=list([1,2,3,4,5,6])

for each in new_columns2:
    try:
        df[each]=[dict(index[each])["label"] for index in df.categoryBreadcrumb]
    except:
        pass    


price=pd.DataFrame(df.iloc[:,13])
df=df.iloc[:,21:52]

df.drop(columns=['live', 'location','locations','originalCurrency',
          'originalPrice','ownerId','price','shortname','status',
          'store','tagAttributes','title', 'userPenaltyScore','a706',
          'a4054','a9620',1,4],inplace=True)

df=np.concatenate((df,price),axis=1)
df=pd.DataFrame(df)
    
df.columns=["Lat","Long","Renk","KM","Yil","Vites","Yakit","Tip","Itis","Beygir","Marka","Model","Fiyat"]

root= tk.Tk()

canvas1 = tk.Canvas(root, width = 300, height = 300, bg = 'lightsteelblue2', relief = 'raised')
canvas1.pack()

def exportCSV ():
    global df
    
    export_file_path = filedialog.asksaveasfilename(defaultextension='.csv')
    df.to_csv (export_file_path, index = None, header=True)

saveAsButton_CSV = tk.Button(text='Export CSV', command=exportCSV, bg='green', fg='white', font=('helvetica', 12, 'bold'))
canvas1.create_window(150, 150, window=saveAsButton_CSV)

root.mainloop()