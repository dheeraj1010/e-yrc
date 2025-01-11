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
pitcher_level =0
def update( a,b,c,d ):


    file = open("ar_data.txt", "w")
    file.write(str(a) + "," + str(b) + "," + str(c) + "," + str(d))
    file.close()



msg_flag = 0
pick_up_state = 0

 # initialise the robot in the arena ----
path.Robot_start = "START-1"
#>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# arena_config = { 0:("pebble", 2, "3-3"),  1: ("pitcher", 9, "2-2")}
arena_config = {0: ("Water Pitcher", 6, "2-2"), 2:("Pebble",8, "3-3"), 4:("Pebble", 16, "2-2"), 6:("Pebble", 19, "1-1")}
ids = list(arena_config)
print( ids )
implement_config= {}
counting = 0
# dictionary for theme implementation by robot
for n in range( 1,len(ids)):
    implement_config[counting] = list(arena_config[ids[n]])
    implement_config[counting].append(ids[n])

    counting= counting+1
    implement_config[counting] = list(arena_config[ids[0]])
    implement_config[counting].append(ids[0])
    counting = counting + 1

print( implement_config)

# >>>>>>>>>>>>>>>>>>>>>>>>> seting up ar<<<<<<<<<<<<<<<<<<<<<<<<<<<


previous_location = path.Robot_start
current_location = (0,0) # update if initial position is not start-1 or start-2
dest = ("","")
count = 0
for target in implement_config: # target is physically the aruco marker here -----
# selecting target ----

    dest =  (implement_config[target][1], implement_config[target][2])
    print("TARGET  is = ", implement_config[target][0],"and cell id = ",implement_config[target][1],"and axis =",implement_config[target][2])
    previous_location, current_location = path.path_planner(previous_location, current_location, dest )

    print("planned string is = ", path.path_string)  # argument ( previous loc , taget:(cell-id ,axis)

    #
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    serial.send_data("s")
    # serial.send_data(":040")
    serial.send_data(":000")
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
                serial.send_data('s')
                msg_flag = 1
                serial.send_data('SS')
                serial.flush_in()
                print("turning : ", turn_value)
                serial.send_data(turn_value)
                serial.delay(1000)
                serial.flush_in()
                break
    serial.send_data("h")
    serial.delay(1)
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@





    file = open("ar_data.txt", "r")
    id_0,id_2,id_4,id_6 = eval(file.read())
    file.close()
    if implement_config[target][0] =="Pebble":
        print("::::::::::::::  PICKUP PROCESS STARTING :::::::::::::::::::")
        path.pick_up()
        if implement_config[target][3] == 2:
            update(id_0,0,id_4,id_6)
        if implement_config[target][3] == 4:
            update(id_0, id_2,0, id_6)
        if implement_config[target][3] == 6:
            update(id_0,id_2 ,id_4, 0)


    if implement_config[target][0] == "Water Pitcher":
        print("::::::::::::::  PICKDOWN PROCESS STARTING :::::::::::::::::::")
        path.pick_down()
        if pitcher_level < 4:

            pitcher_level= pitcher_level + 1
            update(pitcher_level, id_2, id_4, id_6)





    path.path_string.clear()
    count = count+1#
#s
#
#
# print ("++++++++++++++++++++++++++++++++++ finished upto path string +++++++++++++++++++++++++++++++++")
serial.send_data('s')
print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> FINISHED :: ", target, " <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
#





