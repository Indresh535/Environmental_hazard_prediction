from os import device_encoding
import serial
import time
import schedule

device = 'COM3'
mcu = serial.Serial(device,9600)
try:
    print('Reading Data....',device)
    mcu = serial.Serial(device,9600)
except:
    print('Unable to read the data')
    
  
  
def display_value():
    data=mcu.readline()
    data = str(data).split('\\')[0].split("'")[1]
    print(data)
    

schedule.every(10).seconds.do(display_value)
#schedule.every(10).seconds.do(display_value)
         
schedule.run_pending()
time.sleep(1)
    
# def main_func():
#     arduino = serial.Serial('com3', 9600)
#     print('Established serial connection to Arduino')
#     arduino_data = arduino.readline()

#     decoded_values = str(arduino_data[0:len(arduino_data)].decode())
#     list_values = decoded_values.split('x')

#     for item in list_values:
#         list_in_floats.append(float(decoded_values))

#     print(f'Collected readings from Arduino: {list_in_floats}')

#     arduino_data = 0
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