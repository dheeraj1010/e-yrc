'''
* Team Id : 3704
* Author List : Akash Yadav
* Filename: main.py
* Theme: Thirsty Crow
* Functions: None
* Global Variables:None
'''

import serial_data as serial
import path
import augment


msg_flag = 0

 # initialise the robot in the arena ----
path.Robot_start = "START-2"
#>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
arena_config = { 0:("pebble", 2, "3-3"),  1: ("pitcher", 9, "2-2")}
# >>>>>>>>>>>>>>>>>>>>>>>>> seting up ar<<<<<<<<<<<<<<<<<<<<<<<<<<<
augment.pebble ="YES"
augment.pitcher_level = "LOW"

previous_location = path.Robot_start
current_location = (0,0) # update if initial position is not start-1 or start-2
dest = ("","")
count = 0
for target in arena_config: # target is physically the aruco marker here -----
# selecting target ----

    dest =  (arena_config[target][1], arena_config[target][2])
    print("TARGET  is aruco number = ", arena_config[target][0])
    previous_location, current_location = path.path_planner(previous_location, current_location, dest )

    print("planned string is = ", path.path_string)  # argument ( previous loc , taget:(cell-id ,axis)

    #
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    serial.send_data("h")
    serial.delay(100)
    serial.send_data("s")
    serial.send_data(":040")
    serial.send_data(":000")
    serial.send_data("-")
    print("engine on ----")
    print("turning path following mode on ")
    serial.send_data("####")

    for turn_value in path.path_string:
        print("turning path following mode on ")
        serial.send_data("####")
        while (1):
            print(".....waiting for node .....")
            if (serial.get_data(1) == '!'):
                print("...node detected ...")
                serial.send_data('h')
                serial.send_data('s')
                msg_flag = 1
                serial.send_data('SSSS')
                serial.flush_in()
                print("turning : ", turn_value)
                serial.send_data(turn_value)
                serial.delay(2000)
                serial.flush_in()
                break
    serial.send_data("h")
    serial.delay(1)
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    print("::::::::::::::  PICKUP PROCESS STARTING :::::::::::::::::::")
    # path.pick_up()

    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> FINISHED :: ", target, " <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    if arena_config[target][0] == "pebble":
        augment.pebble = "NO"
    if arena_config[target][0] == "pitcher":
        augment.pitcher = "HIGH"

    path.path_string.clear()
    count = count+1#
#
#
#
# print ("++++++++++++++++++++++++++++++++++ finished upto path string +++++++++++++++++++++++++++++++++")
#
#





