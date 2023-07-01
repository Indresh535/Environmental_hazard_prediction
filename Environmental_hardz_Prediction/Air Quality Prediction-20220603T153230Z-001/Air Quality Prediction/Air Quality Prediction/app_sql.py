from flask import Flask,render_template,url_for,request,jsonify

import numpy as np
import pandas as pd
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
import datetime
import pickle
from flask import Flask, request, jsonify, render_template

import joblib
import serial
import time
import schedule


gmail_list=[]
password_list=[]
gmail_list1=[]
password_list1=[]


    

# Load the model from the file 
model = joblib.load('final_pickle_model.pkl')  
modelRain = pickle.load(open("rain_XGBnew_model.pkl", "rb"))
# Use the loaded model to make predictions 



app = Flask(__name__, template_folder='template')


@app.route('/',methods=['GET'])
def home():
    return render_template('index.html')

        
# @app.route('/register',methods=['POST'])
# def register():
    

#     int_features2 = [str(x) for x in request.form.values()]

#     r1=int_features2[0]
#     print(r1)
    
#     r2=int_features2[1]
#     print(r2)
#     logu1=int_features2[0]
#     passw1=int_features2[1]
        
    

    

#    # if int_features2[0]==12345 and int_features2[1]==12345:

#     import MySQLdb


# # Open database connection
#     db = MySQLdb.connect("localhost","root",'',"ddbb" )

# # prepare a cursor object using cursor() method
#     cursor = db.cursor()
#     cursor.execute("SELECT user FROM user_register")
#     result1=cursor.fetchall()


#     for row1 in result1:
#                       print(row1)
#                       print(row1[0])
#                       gmail_list1.append(str(row1[0]))
                      

                      
#     print(gmail_list1)
#     if logu1 in gmail_list1:
#         return render_template('register.html',text="This Username is Already in Use ")

#     else:

                  
              

# # Prepare SQL query to INSERT a record into the database.
#                   sql = "INSERT INTO user_register(user,password) VALUES (%s,%s)"
#                   val = (r1, r2)
   
#                   try:
#    # Execute the SQL command
#                                        cursor.execute(sql,val)
#    # Commit your changes in the database
#                                        db.commit()
#                   except:
#    # Rollback in case there is any error
#                                        db.rollback()

# # disconnect from server
#                   db.close()
#                   return render_template('register.html',text="Succesfully Registered")


# @app.route('/login')
# def login(): 
#     return render_template('login.html')         
                      


# @app.route('/logedin',methods=['POST'])
# def logedin():
#         return render_template('index.html')
                                               


@app.route('/AIQPrediction')
def production(): 
    return render_template('air.html')


@app.route('/AIQPrediction/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    int_features = [str(x) for x in request.form.values()]
    print(int_features)
    a=int_features

  


   
    temp = float(a[0])
    humidity=float(a[1])
    WindSpeed = float(a[2])
    Visibility =float(a[3])
    Pressure = float(a[4])
    so2=float(a[6])                       
    no2=float(a[7])
    Rainfall=float(a[5])
    pm10=float(a[8])
    pm2_5=float(a[9])
    

    data= {'Temperature':[temp],'Humidity':[humidity],'Wind Speed':[WindSpeed],'Visibility':[Visibility],'Pressure':[Pressure],'so2':[so2],'no2':[no2],'Rainfall':[Rainfall],'pm10':[pm10],'pm2_5':[pm2_5]} 
    df = pd.DataFrame(data)
      
# Print the output. 
    print(df )



    prediction=model.predict(df)
    prediction=int(prediction)


    

    if((prediction>=0) and (prediction<=50)):
        return render_template('air.html',prediction_text='Air Quality Index  is {}'.format(prediction),prediction_text1='Air Quality is Good')
        
        
    
    if((prediction>=51) and (prediction<=100)):
        return render_template('air.html',prediction_text='Air Quality Index   is {}'.format(prediction),prediction_text1='Air Quality is Moderate')
       
     
        
    if((prediction>=101) and (prediction<=150)):
        return render_template('air.html',prediction_text='Air Quality Index  is {}'.format(prediction),prediction_text1='Air Quality is Unhealthy')
       
       
        
    if((prediction>=151) and (prediction<=200)):
        return render_template('air.html',prediction_text='Air Quality Index   is {}'.format(prediction),prediction_text1='Air Quality is Unhealthy for Strong People')
        
        
    if(prediction>201):
        return render_template('air.html',prediction_text='Air Quality Index  is {}'.format(prediction),prediction_text1='Air Quality is Hazaradous')
       
        

@app.route("/rain",methods=['GET'])

def rain():
	return render_template("rain.html")

@app.route("/predict",methods=['GET', 'POST'])
def predictRain():
	if request.method == "POST":
		# DATE
		date = request.form['date']
		day = float(pd.to_datetime(date, format="%Y-%m-%dT").day)
		month = float(pd.to_datetime(date, format="%Y-%m-%dT").month)
		# MinTemp
		minTemp = float(request.form['mintemp'])
		# MaxTemp
		maxTemp = float(request.form['maxtemp'])
		# Rainfall
		rainfall = float(request.form['rainfall'])
		# Evaporation
		evaporation = float(request.form['evaporation'])
		# Sunshine
		sunshine = float(request.form['sunshine'])
		# Wind Gust Speed
		windGustSpeed = float(request.form['windgustspeed'])
		# Wind Speed 9am
		windSpeed9am = float(request.form['windspeed9am'])
		# Wind Speed 3pm
		windSpeed3pm = float(request.form['windspeed3pm'])
		# Humidity 9am
		humidity9am = float(request.form['humidity9am'])
		# Humidity 3pm
		humidity3pm = float(request.form['humidity3pm'])
		# Pressure 9am
		pressure9am = float(request.form['pressure9am'])
		# Pressure 3pm
		pressure3pm = float(request.form['pressure3pm'])
		# Temperature 9am
		temp9am = float(request.form['temp9am'])
		# Temperature 3pm
		temp3pm = float(request.form['temp3pm'])
		# Cloud 9am
		cloud9am = float(request.form['cloud9am'])
		# Cloud 3pm
		cloud3pm = float(request.form['cloud3pm'])
		# Cloud 3pm
		location = float(request.form['location'])
		if(location == 'Portland'):
			location = 1
		elif(location == 'Cairns'):
			location = 2
		elif(location == 'Walpole'):
			location = 3
		elif(location == 'Dartmoor'):
			location = 4
		elif(location == 'MountGambier'):
			location = 5
		elif(location == 'NorfolkIsland'):
			location = 6
		elif(location == 'Albany'):
			location = 7
		elif(location == 'Witchcliffe'):
			location = 8
		elif(location == 'CoffsHarbour'):
			location = 9
		elif(location == 'Sydney'):
			location = 10
		elif(location == 'Darwin'):
			location = 11
		elif(location == 'MountGinini'):
			location = 12
		elif(location == 'NorahHead'):
			location = 13
		elif(location == 'Ballarat'):
			location = 14
		elif(location == 'GoldCoast'):
			location = 15
		elif(location == 'SydneyAirport'):
			location = 16
		# Wind Dir 9am
		winddDir9am = float(request.form['winddir9am'])
		if(winddDir9am == 'NMW'):
			winddDir9am == 0
		elif(winddDir9am== 'NW'):
			winddDir9am == 1
		elif(winddDir9am== 'WNW'):
			winddDir9am == 2
		elif(winddDir9am== 'N'):
			winddDir9am == 3
		# Wind Dir 3pm
		winddDir3pm = float(request.form['winddir3pm'])
		if(winddDir3pm== 'NW'):
			winddDir3pm == 0
		elif(winddDir3pm== 'NNW'):
			winddDir3pm == 1
		elif(winddDir3pm == 'N'):
			winddDir9am == 2
		elif(winddDir3pm== 'WNW'):
			winddDir3pm == 3
		# Wind Gust Dir
		windGustDir = float(request.form['windgustdir'])
		if(windGustDir== 'NNW'):
			windGustDir == 0
		elif(windGustDir == 'NW'):
			windGustDir == 1
		elif(windGustDir== 'WNW'):
			windGustDir == 2
		elif(windGustDir== 'N'):
			windGustDir == 3
		# Rain Today
		rainToday = float(request.form['raintoday'])
		if(rainToday== 'Yes'):
			rainToday== 1
		elif(rainToday== 'No'):
			rainToday== 0

		input_lst = [location , minTemp , maxTemp , rainfall , evaporation , sunshine ,
					 windGustDir , windGustSpeed , winddDir9am , winddDir3pm , windSpeed9am , windSpeed3pm ,
					 humidity9am , humidity3pm , pressure9am , pressure3pm , cloud9am , cloud3pm , temp9am , temp3pm ,
					 rainToday , month , day]
		input_lst = np.array(input_lst).reshape((1,-1))
		pred = model.predict(input_lst)
		output = pred

	if output == 0:
		return render_template("after_sunny.html")
	else:
		return render_template("after_rainy.html")  


    


if __name__ == "__main__":
    app.run(debug=True)
    
  



 
    



# import serial
# import time
# import schedule


# def main_func():
#     arduino = serial.Serial('com3', 9600)
#     print('Established serial connection to Arduino')
#     arduino_data = arduino.readline()

#     decoded_values = str(arduino_data[0:len(arduino_data)].decode("utf-8"))
#     list_values = decoded_values.split('x')

#     for item in list_values:
#         list_in_floats.append(float(item))

#     print(f'Collected readings from Arduino: {list_in_floats}')

#     arduino_data = 0
#     list_in_floats.clear()
#     list_values.clear()
#     arduino.close()
#     print('Connection closed')
#     print('<----------------------------->')


# # ----------------------------------------Main Code------------------------------------
# # Declare variables to be used
# list_values = []
# list_in_floats = []

# print('Program started')

# # Setting up the Arduino
# schedule.every(10).seconds.do(main_func)

# while True:
#     schedule.run_pending()
#     time.sleep(1)