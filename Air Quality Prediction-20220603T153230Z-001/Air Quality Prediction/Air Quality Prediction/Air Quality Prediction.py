# for numerical computing
import numpy as np

# for dataframes
import pandas as pd


# Ignore Warnings
import warnings
warnings.filterwarnings("ignore")



# to split train and test set
from sklearn.model_selection import train_test_split




import sklearn.metrics as sm





df=pd.read_csv('Dataset1.csv')
print(df.shape)
print(df.columns)
print(df.head())
print(df.describe())
print(df.corr())
df = df.drop_duplicates()
print( df.shape )
print(df.isnull().sum())
df=df.dropna()
print(df.isnull().sum())



y = df.AQI
X = df.drop('AQI', axis=1)




# Split X and y into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y,  test_size=0.2, random_state=0)


# Print number of observations in X_train, X_test, y_train, and y_test
print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)





from sklearn.ensemble import RandomForestRegressor

model1 = RandomForestRegressor()

from sklearn.linear_model import LinearRegression

model2 = LinearRegression()  


model1.fit(X_train, y_train)

model2.fit(X_train, y_train)



## Predict Test set results
y_pred1 = model1.predict(X_test)
y_pred2 = model2.predict(X_test)



df1 = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred1})  

print(df1)



y_pred1=np.array(y_pred1).reshape(-1,1)


y_pred2=np.array(y_pred2).reshape(-1,1)



accuracy=sm.r2_score(y_test,y_pred1)
      
print("Accuracy of RandomForestRegressor is  {:.2f} % ".format(accuracy*100))


accuracy=sm.r2_score(y_test,y_pred2)
      
print("Accuracy of Linear Regression is {:.2f} % ".format(accuracy*100))




#from  import joblib 
import joblib
# Save the model as a pickle in a file 
joblib.dump(model1, 'final_pickle_model.pkl') 
  
# Load the model from the file 
final_model= joblib.load('final_pickle_model.pkl')

pred=final_model.predict(X_test)

accuracy=sm.r2_score(y_test,pred)
      
print("Accurcay of Final Model is {:.2f} % ".format(accuracy*100))



       
        

