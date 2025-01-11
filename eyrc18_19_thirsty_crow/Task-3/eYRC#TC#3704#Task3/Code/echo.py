'''
* Team Id : 3704
* Author List : Akash Yadav
* Filename: echo.py
* Theme: Thirsty Crow
* Functions: None
* Global Variables:None 
'''


import serial 
import time


if __name__ == "__main__":
    ser = serial.Serial("COM6", 9600, timeout=.09)

    while True:
        user_input = input("Enter key: ")
        
        
        
        ########## ENTER YOUR CODE HERE ############

        # String to binary conversion and sending to serial .
        ser.write((eval("b'{x}'".format(x=user_input))))

        
        # data_rx : data received from serial
        data_rx = ser.readline()
        if (str(data_rx) == "b''"):
            # in case avr is off ( NO RESPONSE ).
            print ("---------NO RESPONSE FROM SERIAL --------")
            
        else :
            print (data_rx)
    
            
        
        


        ############################################
