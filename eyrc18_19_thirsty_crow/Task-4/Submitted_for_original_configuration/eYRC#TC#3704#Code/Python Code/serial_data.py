'''
* Team Id : 3704
* Author List : Akash Yadav
* Filename: serial_data.py
* Theme: Thirsty Crow
* Functions: delay,send_data,get_data,flush_in
* Global Variables:data , ser
'''

import serial
import time
data = '\0'
#seting port for serial communication
ser = serial.Serial("COM3", 9600,timeout=0.4 )

"""
Function Name : delay()
Input: time delay
Output: 
Purpose: provides delay functionality
"""

def delay(secs):
    # delay in --seconds
    time.sleep(secs/1000)

"""
Function Name : send_data()
Input: user_input (data to be sent serially )
Output: 
Purpose: sends data to robot 
"""
def send_data (user_input ):
  #  user_input = (input("Enter key: "))
    # String to binary conversion and sending to serial .

    ser.write((eval("b'{x}'".format(x=(user_input)))))
    delay(1500) # delay can be varied upon further testing transmission time

"""
Function Name :get_data()
Input: bytes to be read 
Output: serial data
Purpose: to receive data from robot 
"""
def get_data(length):
    # data_rx : data received from serial

    data_rx = ser.read_until(size=length)
    string =[]
    if (str(data_rx) == "b''"):
        # in case avr is off ( NO RESPONSE ).
        print("---------")
    else:
        #print(data_rx)
        string = list(str(data_rx))
        string=''.join(string[2:len(string)-1])

    return string


"""
Function Name : flush_in()
Input: 
Output: 
Purpose: to flush input serial buffer 
"""
def flush_in():
    ser.flushInput()


