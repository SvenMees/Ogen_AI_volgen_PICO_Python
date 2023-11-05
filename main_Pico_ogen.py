#example usage of the Simply Servos class - sets all servos to 0 then 180

from symplyServos import KitronikSimplyServos
import time
from time import sleep
from machine import Pin,UART

import random


uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

uart.init(bits=8, parity=None, stop=1)

def knipper():
    servos.goToPosition(onderlidrechts,75)
    servos.goToPosition(bovenlidrechts,75)
    servos.goToPosition(onderlidlinks,180)
    servos.goToPosition(bovenlidlinks,90)
    sleep(0.2)
    #knipper naar open stand
    servos.goToPosition(onderlidrechts,170)
    servos.goToPosition(bovenlidrechts,35)
    servos.goToPosition(onderlidlinks,100)
    servos.goToPosition(bovenlidlinks,140)
    sleep(0.2)
    
    
def knipperboos():
    servos.goToPosition(onderlidrechts,115)  # 75 tot 180
    servos.goToPosition(bovenlidrechts,45)    #0 tot 100
    servos.goToPosition(onderlidlinks,150) #80 tot 180
    servos.goToPosition(bovenlidlinks,120)   # 100 tot 180
    sleep(3)
    #knipper naar open stand
    servos.goToPosition(onderlidrechts,170)
    servos.goToPosition(bovenlidrechts,35)
    servos.goToPosition(onderlidlinks,100)
    servos.goToPosition(bovenlidlinks,140)
    sleep(0.2)
    
def knipperslaap():
    servos.goToPosition(onderlidrechts,80)  # 75 tot 180
    servos.goToPosition(bovenlidrechts,45)    #0 tot 100
    servos.goToPosition(onderlidlinks,170) #80 tot 180
    servos.goToPosition(bovenlidlinks,120)   # 100 tot 180
    sleep(3)
    #knipper naar open stand
    servos.goToPosition(onderlidrechts,170)
    servos.goToPosition(bovenlidrechts,35)
    servos.goToPosition(onderlidlinks,100)
    servos.goToPosition(bovenlidlinks,140)
    sleep(0.2)

servos = KitronikSimplyServos()
x = 1
onderlidrechts= 3    #100 tot 180
onderlidlinks= 5  #80 tot 180
bovenlidrechts= 1  #0 tot 100 max
bovenlidlinks= 2  #100 tot 180
ooglinksrechts = 4 #20 tot 120
oogbovenonder = 0  #50 tot 120
print("hallo")

knipper()
getalx = 65
getaly = 65
deler= 8
x= "A65A65A"
while True:
        knip = random.randint(1, 500)
        if uart.any(): 
            data = uart.read()
            
            uart.write(data)
            eenstring = str(data)
            x = eenstring.split("A")   #verdeel in 3 delen
            
            print(len(x))
            print(x[0])
            print(x[1])
            
            try:
                getalx = int(x[1])
                getaly = int(x[2])
            except ValueError:
                print("some_variable did not contain a number!")
            

              
          
        servos.goToPosition(ooglinksrechts,getaly)  #20 tot 120
        servos.goToPosition(oogbovenonder,getalx)  #50 tot 120
        
        
        if knip == 4:
            knipper()

       
        
             

        
        
        
