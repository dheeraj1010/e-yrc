"""
* Team Id : 3704
* Author List : Akash Yadav
* Filename: path.py
* Theme: Thirsty Crow
* Functions: None
* Global Variables: path_string
"""

import serial_data as serial
import numpy as np
import math as mt
import camera as cam

path_string =[] # source to destination path in form of string ....
#side length
length = 23 # in cm
a = length*mt.sqrt(3)  # inter_node distance

out_rad_1 = mt.sqrt( (4.5*length)**2 + (cam.cos(30)*length)**2)
th1 = 10.8933946
out_rad_2 = mt.sqrt( (3*length)**2 + ((4*cam.cos(30))*length)**2)
th2 = 49.10660535
out_rad_3 =  mt.sqrt( (1.5*length)**2 + ((5*cam.cos(30))*length)**2)
th3 = 70.89339465

Robot_start = ""
# it is basic requirement to assign coordinates to respective cells for path planning algorithm to work ---
#cell data in polar form (r,theta(in degree) )cell_7 center as origin --
cell_data = {1:(2*a,90)  ,2:(2*a*cam.cos(30),120)  ,3:(a,90)  ,4:(2*a*cam.cos(30),60)  ,5:(2*a,150)  ,6:(a,150),7:(0,0),8:(a,30),9:(2*a,30),10:(2*a*cam.cos(30),180),11:(a,210),12:(a,270),13:(a,330),14:(2*a*cam.cos(30),0),15:(2*a,210),16:(2*a*cam.cos(30),240),17:(2*a,270),18:(2*a*cam.cos(30),300),19:(2*a,330),20:(out_rad_1,th1),21:(out_rad_2,th2),22:(out_rad_3,th3),23:(out_rad_3,180-th3),24:(out_rad_2,180-th2),25:(out_rad_1,180-th1),26:(out_rad_1,180+th1),27:(out_rad_2,180+th2),28:(out_rad_3,180+th3),29:(out_rad_3,360-th3),30:(out_rad_2,360-th2),31:(out_rad_1,360-th1),32:(3*a,30),33:(3*a,90),34:(3*a,150),35:(3*a,210),36:(3*a,270),37:(3*a,330)}

#setting co-ordinate system



"""
Function Name : region ()
Input: 
Output: 
Purpose: to compare points distance in accurate way ( circular domain)
"""
def region(center_point , comp_point , rad  ):
    center_x ,center_y = center_point
    comp_x , comp_y = comp_point
    centerTopoint_dist = mt.sqrt((center_x-comp_x)**2 + (center_y-comp_y)**2)
    if centerTopoint_dist >rad :
        return 0  # point lie in region
    if centerTopoint_dist <= rad :
        return 1  # point does not lie in region

"""
Function Name : polar_cart ()
Input: polar coordinate
Output: carstesian  system
Purpose: to convert polar coordinate to carstesian  system
"""
def polar_cart(point):
    r,theta = point
    x = round (r*cam.cos(theta),4)
    y = round (r*cam.sin(theta),4)
    return (x,y)
"""
Function Name : distance_polar ()
Input: polar coordinates
Output: distance 
Purpose: to get distance between two points 
"""
def distance_polar(point1, point2):
    # verified
        # argument is in polar form

        r1, th1 = point1
        r2, th2 = point2

        dist  = mt.sqrt(((r2 * cam.cos(th2) - r1 * cam.cos(th1)) ** 2) +( (r2 * cam.sin(th2) - r1 * cam.sin(th1)) ** 2))

        return dist

"""
Function Name : distance_cart ()
Input: cartesian coordinates
Output: distance 
Purpose: to get distance between two points 
"""

def distance_cart( point1,point2 ):
    # verified
    # argument in cartesian form
    x1,y1 = point1
    x2,y2 = point2
    dist = mt.sqrt ( (x2-x1)**2 + (y2-y1)**2)
    return dist


"""
Function Name : cell_minima()
Input: current location 
Output: list of cells at minimum distance 
Purpose:to get list of cells at minimum distance 
"""
def cell_minima(current_loc,obj):
#objects are cell and nodes ---- for cell obj = C :: --- for node obj = N
#for cell pass the polar in argument and for nodes cartesian form is expected as input
#tells us the least distant cell center..

    dist = np.zeros(37, float)
    min_data = np.zeros(7, int)
    if obj =='C':
        #polar

        for i in range(1, 38):
            dist[i - 1] = round(distance_polar( current_loc, cell_data[i]), 1)


    if obj =='N':
        # cartesian

        # print ("accepting cartesian --NODE mode ")

        for i in range(1, 38):
            r,theta= cell_data[i]
            cell_x = r * cam.cos(theta)
            cell_y = r*  cam.sin(theta)
            dist[i - 1] = round(distance_cart( current_loc,(cell_x,cell_y) ), 3)

    minimum=np.min(dist)
    print ("dist",dist)
    print ("minimum",minimum)
    j=0
    for i in range (0,37):
        if  dist[i]- minimum <8:
            min_data[j]=i+1
            j= j+1
# =return type is list
    print ("....cell min accesed ...")
    print ("min_data from --cell_minima --- ",min_data)
    return min_data


"""
Function Name : light ()
Input: cell id  
Output: list of cells nodes coordinates
Purpose:
"""

def light(cell_id,acc) :
    # shines the dark corners ...
    r_cell,th_cell = cell_data[cell_id] # coordinates of cell center of given cell ...
    x_cell = r_cell*cam.cos(th_cell)
    y_cell = r_cell*cam.sin(th_cell)
#nodes = np.zeros((2,6),float)# storing data of nodes corresponding to given cell..
    nodes={}
    for i in range(0,6):

        nodes[i+1]= round((x_cell+(length*cam.cos(60*i))),acc),round((y_cell+(length*cam.sin(60*i))),acc)
# retun type is dictionary
    return nodes


def double_light (cell_id,acc) :
    # shines the dark corners ...
    r_cell,th_cell = cell_data[cell_id] # coordinates of cell center of given cell ...
    x_cell = r_cell*cam.cos(th_cell)
    y_cell = r_cell*cam.sin(th_cell)
#nodes = np.zeros((2,6),float)# storing data of nodes corresponding to given cell..
    nodes={}
    for i in range(0,6):
        nodes[i+1]= round((x_cell+(2*length*cam.cos(60*i))),acc),round((y_cell+(2*length*cam.sin(60*i))),acc)


# retun type is dictionary

    return nodes



"""
Function Name : node_selecter()
Input:previous location, current location ,destination, target
Output:selected node , selected cell
Purpose:
"""
def node_selecter( previous_loc ,current_loc , destination ,target_cell ):
    previous_loc = list( previous_loc)
    previous_loc[0]=  round( previous_loc[0],0)
    previous_loc[1] = round(previous_loc[1], 0)
    previous_loc = tuple(previous_loc)

    current_loc = list(current_loc)
    current_loc[0] = round(current_loc[0], 0)
    current_loc[1] = round(current_loc[1], 0)
    current_loc = tuple(current_loc)

    # print ( "comp pre ",previous_location)
    # NOTE -- all arguments expected in cartesian system
    possible_cells = []

    for cell in cell_minima(current_loc,'N') :
        if cell!= 0 :
            possible_cells.append(cell)


    while ( len(possible_cells)>1):
        print(" possible cell before remove  = ", possible_cells)
        for cell in possible_cells:
            print("..........cell ", cell, " nodes being cheaked .........")
            read_node = light(cell, 0)  # dictionary of nodes
            print("node data of cell ", cell, "is = ", read_node)
            for node in read_node:
                if region(read_node[node], previous_loc, 15) == 1:
                    print(" ---cell is rejected--- >> ", cell)
                    possible_cells.remove(cell)
    if  len(possible_cells)==1:
        print(" possible cell after remove  = ", possible_cells)
        proposed_cell = possible_cells[0]  # final cell selected
        print(" proposed cell = ", proposed_cell)
        print ("######################   DONE ( ALL GOOD ) ###########################")


    hex_local = 0 # localised node on hexagon
    hex_a=0
    hex_b=0
    j=0
    nodes_cell = light(proposed_cell,0)

    print ("nodes -- ",nodes_cell)

    for j in range(1,7):
        if  region(nodes_cell[j],current_loc,5) ==1:
            print("localised node = ", j)
            hex_local =j

    if hex_local==1:
        hex_a= 2
        hex_b =6
    if hex_local==6:
        hex_a= 1
        hex_b =5
    if hex_local !=1 and hex_local !=6:
        hex_a = hex_local+1
        hex_b = hex_local-1
        print ("hex_a = ",hex_a) #hex_a is right wrt robot
        print ("hex_b = ",hex_b) #hex_b is left wrt robot

    node_error = 0
    selected_node = 0
    hex_a_to_dst = distance_cart(nodes_cell[hex_a], destination)
    hex_b_to_dst = distance_cart(nodes_cell[hex_b], destination)
    # decieding left or right  ..
    #comparing distances of hex_a and hex_b to destination point ...
    ## cheaking if hex_a or hex_b lies on target cell..
    if (target_cell !=0):

        read_node_data = light(target_cell, 0)  # dictionary of nodes
        print("node data of target - cell ", cell, "is = ", read_node_data)
        for node in read_node_data:
            if region(read_node_data[node], light(proposed_cell,3)[hex_a], 15) == 1:
                print(" ---hex_a is rejected---lies in target cell >> ")
                node_error =1
                selected_node = hex_b
                path_string.append('L')
                break

            if region(read_node_data[node], light(proposed_cell, 3)[hex_b], 15) == 1:
                print(" ---hex_b is rejected---lies in target cell >> ")
                node_error = 1
                selected_node = hex_a
                path_string.append('R')
                break
    if (node_error==1):
        print("++++++++++++++++++++++++++ ERROR FLAG ACTIVATED +++++++++++++++++++++++++++", node_error)
        print("+++++++++++++target cell is = ", target_cell)


    if (node_error==0):
        # choosing node leading to shortest path...
        if (hex_a_to_dst <= hex_b_to_dst):
            # pass move right command
            path_string.append('R')
            selected_node = hex_a
        if (hex_b_to_dst < hex_a_to_dst):
            # pass move left command
            path_string.append('L')
            selected_node = hex_b


    print("path-planned >> ",path_string)

    return proposed_cell,selected_node


"""
Function Name :endpoint2()
Input:
Output: initial endpoint 
Purpose:
"""
def endpoint2( cell, orientation,current_loc ):

    limit = 3*a
    if (orientation == "3-3"):
        points = [  double_light(cell,3)[2], double_light(cell,3)[5] ]
        if distance_cart(points[0],current_loc)<distance_cart(points[1],current_loc):
            print("point 0 ", points[0])
            if (distance_cart((0,0),points[0]))<= limit :
                return points[0]
            else :
                return points[1]
        if distance_cart(points[1], current_loc) <distance_cart(points[0], current_loc):
            print("point 0 ", points[1])
            if (distance_cart((0,0),points[0]))<= limit :
                return points[1]
            else :
                return points[0]
    if (orientation == "1-1"):
        points = [double_light(cell,3)[1], double_light(cell,3)[4]]
        if distance_cart(points[0],current_loc)<distance_cart(points[1],current_loc):
            print("point 0 ", points[0])
            if (distance_cart((0,0),points[0]))<= limit :
                return points[0]
            else :
                return points[1]
        if distance_cart(points[1], current_loc) <distance_cart(points[0], current_loc):
            print("point 0 ", points[1])
            if (distance_cart((0,0),points[0]))<= limit :
                return points[1]
            else :
                return points[0]
    if (orientation == "2-2"):
        points = [double_light(cell,3)[6], double_light(cell,3)[3]]
        if distance_cart(points[0],current_loc)<distance_cart(points[1],current_loc):
            print("point 0 ", points[0])
            if (distance_cart((0,0),points[0]))<= limit :
                return points[0]
            else :
                return points[1]
        if distance_cart(points[1], current_loc) <distance_cart(points[0], current_loc):
            print("point 0 ", points[1])
            if (distance_cart((0,0),points[0]))<= limit :
                return points[1]
            else :
                return points[0]
"""
Function Name :endpoint1()
Input:
Output: final endpoint located in cell
Purpose:
"""
def endpoint1( cell, orientation,current_loc ):

    limit = 3*a
    if (orientation == "3-3"):
        points = [ light(cell,3)[2], light(cell,3)[5] ]
        if distance_cart(points[0],current_loc)<distance_cart(points[1],current_loc):
            print("point 0 ", points[0])
            if (distance_cart((0,0),points[0]))<= limit :
                return points[0]
            else :
                return points[1]
        if distance_cart(points[1], current_loc) <distance_cart(points[0], current_loc):
            print("point 0 ", points[1])
            if (distance_cart((0,0),points[0]))<= limit :
                return points[1]
            else :
                return points[0]
    if (orientation == "1-1"):
        points = [light(cell,3)[1], light(cell,3)[4]]
        if distance_cart(points[0],current_loc)<distance_cart(points[1],current_loc):
            print("point 0 ", points[0])
            if (distance_cart((0,0),points[0]))<= limit :
                return points[0]
            else :
                return points[1]
        if distance_cart(points[1], current_loc) <distance_cart(points[0], current_loc):
            print("point 0 ", points[1])
            if (distance_cart((0,0),points[0]))<= limit :
                return points[1]
            else :
                return points[0]
    if (orientation == "2-2"):
        points = [light(cell,3)[6], light(cell,3)[3]]
        if distance_cart(points[0],current_loc)<distance_cart(points[1],current_loc):
            print("point 0 ", points[0])
            if (distance_cart((0,0),points[0]))<= limit :
                return points[0]
            else :
                return points[1]
        if distance_cart(points[1], current_loc) <distance_cart(points[0], current_loc):
            print("point 0 ", points[1])
            if (distance_cart((0,0),points[0]))<= limit :
                return points[1]
            else :
                return points[0]
"""
Function Name :path_planner()
Input: 
Output: previous location , current location 
Purpose: to get planned path between initial and final point
"""
def path_planner(previous_loc ,current_loc ,target  ):
    # previous_loc and current_loc is expected to be (cell,node )  system
     # destination is cell id here and optimized target is auto -generated --



    if previous_loc == "START-1" or  previous_loc == "START-2":
        START_1 = light(25,3)[5]
        START_2 = (115,0)#light(31,2)[5]


        if previous_loc == "START-1":
            current_location =light (10,3)[4]
            previous_location = START_1
        if previous_loc =="START-2":
            previous_location = START_2
            current_location =light (14,3)[1]
    else :

        previous_location = previous_loc #light(previous_loc[0], 3)[previous_loc[1]]
        current_location  = current_loc# light(current_loc[0], 3)[current_loc[1]]


    target_cell,axis = target

    destination = endpoint2( target_cell, axis, current_location )  # endpoint(9,"2-2",current_location)

    while distance_cart(current_location, destination) > 3:
        cell, sel_node = node_selecter(previous_location, current_location, destination,target_cell)#predicted location
        print ("predicted location cell -id = ",cell,sel_node)
        predicted_location = light(cell, 5)[sel_node]
        print("curret_loc", current_location)
        print("predicted  loc", predicted_location)
        previous_location = current_location
        current_location = predicted_location
        print("DISTANCE SRC-DST = ", round(distance_cart(current_location, destination), 1))

    print ("PICKP-ZONE  --- DESTINATION UPDATED ")



    destination = endpoint1( target_cell, axis, current_location )
    cell, sel_node = node_selecter(previous_location, current_location, destination,0)
    # predicted location

    # while distance_cart(current_location, destination) > 5:
    #     cell, sel_node = node_selecter(previous_location, current_location, destination)#predicted location
    predicted_location = light(cell, 5)[sel_node]
    print("curret_loc", current_location)
    print("predicted  loc", predicted_location)
    previous_location = current_location
    current_location = predicted_location
    print("DISTANCE SRC-DST = ", round(distance_cart(current_location, destination), 1))
    path_string.append("s")
    return previous_location,current_location

#
# def pickup_planner( previous_loc ,current_loc ,target ):



    #

"""
Function Name :pick_up()
Input: 
Output: 
Purpose: for pick_up process 
"""



def pick_up():
    serial.send_data(":090")

    serial.delay(500)
    serial.send_data(":000")

    serial.send_data('s')

