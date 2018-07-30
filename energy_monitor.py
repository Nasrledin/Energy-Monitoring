# !/usr/bin/env python
# import required libraries
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from time import sleep, gmtime, strftime, localtime
import datetime
import os
import minimalmodbus

#--------------------------------------------------------------------------------
#       Initialization
#---------------------------------------------------------------------------------

#$$$    1. LOG File setup       $$$$

#file = open("/home/pi/SDM120/energy_logger.log","r")  # open the log file to read the last logge$
#size =  os.stat("/home/pi/SDM120/energy_logger.log").st_size  # get the size of the log file
#if os.stat("/home/pi/SDM120/energy_logger.log").st_size == 0:
#file_list = file.readlines()
#last_value = file_list[len(file_list)-1] # get the last entry  in the log file 'button.log'
#print "Last logged value is: ", last_value
#file.close()

#$$$    2. Minimalmodbus setup  $$$

instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1) # USB port, Slave ID
instrument.serial.baudrate =9600                        # Baudrate setup
instrument.serial.timeout = 1

#$$$    3. Setup of gspread to connect to google sheet $$$

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('rpi_googlesheet.json', scope) # rpi_$
client = gspread.authorize(creds)
sheet = client.open('Counter')  # Google Spreadsheet name 'Counter'
worksheet = sheet.worksheet("Sheet1") # Worksheet name 'Sheet1'
#data = sheet.get_all_records() # import all data in the accessed google sheet

#--------------------------------------------------------------------------------------------
#        Main loop for reading measurements from the SDM120 meter
#--------------------------------------------------------------------------------------------

def read_voltage():                             # Read voltage function
        V = instrument.read_float(0,4,2)        # Modbus start register for voltage '0' in "V"
        data = round(V,2)
        return data

def read_current():                             # Read current function
        I = instrument.read_float(6,4,2)        # Modbus start register for current '6' in "A"
        data = round(I,2)
        return data

def read_active_power():                        # Read Active power function
        P = instrument.read_float(12,4,2)       # Modbus start register for active power '12' in "W"
        data = round(P,2)
        return data

def read_apparent_power():                      # Read Apparent power function
        S = instrument.read_float(18,4,2)       # Modbus start register for apparent power '18' in "VA"
        data = round(S,2)
        return data

def read_reactive_power():                      # Read Reactive power function
        Q = instrument.read_float(24,4,2)       # Modbus start register for apparent power '24' "VAr"
        data = round(Q,2)
        return data

def read_max_power():                          # Read Maximum total power demand function
        Pmax = instrument.read_float(86,4,2)   # Modbus start register for maximum total power demand '86' in "W"
        data = round(Pmax,2)
        return data

def read_total_energy():                       # Read Total active energy function
        E = instrument.read_float(342,4,2)     # Modbus start register for total active energy '342' in "kWh"
        data = round(E,2)
        return data


def log_data():                          # Data logging  function to log electrical parameters into log file 'energy_logger.log'
        file = open("/home/pi/SDM120/energy_logger.log","a")
        now = strftime("%d %b %Y %H:%M:%S", localtime()) # get current timestamp
        file.write(str(now)+","+str(read_voltage())+","+str(read_current())+","+str(read_active_power())+","+str(read_total_energy())+"\n")
        file.flush()
        file.close()

#$$$            main loop               $$$#

#while True:
now = strftime("%d %b %Y %H:%M:%S", localtime()) # get current timestamp
data_set = [now, read_voltage(), read_current(), read_active_power(), read_total_energy()]      # data package to be sent to Google sheet
worksheet.append_row(data_set)  # append the targetted google sheet with the above data set
log_data()      # recall log_data function that logs the energy measurement to Log file 'energy_logger.log'
