clear all
close all
clc
global A = csvread('sensor_data.csv');  #do not change this line
################################################
#######Declare your global variables here#######

global acc_raw;
global gyro_raw;
global acc_filter;
global gyro_filter;



################################################


function read_accel(axl,axh,ayl,ayh,azl,azh)  
    global acc_raw
    f_cut = 10 ;
    #################################################
    ####### Write a code here to combine the ########
    #### HIGH and LOW values from ACCELEROMETER #####
    ax = typecast(uint8([axl,axh]),'uint16'); 
    ay = typecast(uint8([ayl,ayh]),'uint16'); 
    az = typecast(uint8([azl,azh]),'uint16'); 
    acc_raw = [ acc_raw ; ax ay az ];
    
    
    
    #################################################
    
    
    ####################################################
    # Call function lowpassfilter(ax,ay,az,f_cut) here #
    
    lowpassfilter(ax,ay,az,f_cut)
    
    ####################################################
    
endfunction

function read_gyro(gxl,gxh,gyl,gyh,gzl,gzh)
    global gyro_raw
    f_cut = 10 ;
    #################################################
    ####### Write a code here to combine the ########
    ###### HIGH and LOW values from GYROSCOPE #######
    
    
    gx = typecast(uint8([gxl,gxh]),'uint16'); 
    gy = typecast(uint8([gyl,gyh]),'uint16'); 
    gz = typecast(uint8([gzl,gzh]),'uint16'); 
    
    gyro_raw = [ gyro_raw ; gx gy gz ];
    
    #################################################
    
    
    #####################################################
    # Call function highpassfilter(ax,ay,az,f_cut) here #
    
   highpassfilter(gx,gy,gz,f_cut)
    
    #####################################################;
    
endfunction



function lowpassfilter(ax,ay,az,f_cut)
    dT = .01;  #time in seconds
    Tau = (1/2)*pi*f_cut ;
    alpha = dT/(Tau+dT);                #do not change this line( changed dT should be in numerator )  
    
    ################################################
    ##############Write your code here##############
    global acc_raw;
    global gyro_raw;
    global acc_filter;
    global gyro_filter;
    global A;
    if rows(acc_filter) ==0 
    acc_filter = [ acc_raw(1,1) acc_raw(1,2) acc_raw(1,3) ]
    
    else 
    
        ax_fil = alpha*ax + (1- alpha )* acc_filter(rows(acc_filter),1);
        ay_fil = alpha*ay + (1- alpha )* acc_filter(rows(acc_filter),2);
        az_fil = alpha*az + (1- alpha )* acc_filter(rows(acc_filter),3);
        acc_filter = [ acc_filter ; ax_fil ay_fil az_fil ];
 
    endif 
    
    
    
    
    ################################################
    
endfunction



function highpassfilter(gx,gy,gz,f_cut)
    dT = 0.01;  #time in seconds
    Tau= (1/2)*pi*f_cut ;
    alpha = Tau/(Tau+dT);                #do not change this line
    
    ################################################
    ##############Write your code here##############
    global acc_raw;
    global gyro_raw;
    global acc_filter;
    global gyro_filter;
    global A;
 
    if rows(gyro_filter) ==0 
    gyro_filter= [  gyro_raw(1,1)  gyro_raw(1,2)  gyro_raw(1,3)  ]
  
    else
   
        gx_fil = alpha*gyro_filter(rows(gyro_filter),1)+ alpha* ( gx - gyro_raw(rows(gyro_filter),1)  );
        gy_fil= alpha*gyro_filter(rows(gyro_filter),2)+ alpha*  ( gx - gyro_raw(rows(gyro_filter),2)  );
        gz_fil = alpha*gyro_filter(rows(gyro_filter),3)+ alpha* ( gx - gyro_raw(rows(gyro_filter),3)  );
        
        gyro_filter = [gyro_filter ; gx_fil gy_fil gz_fil   ];
       
    endif 
    
    
    ################################################
    
endfunction

function comp_filter_pitch(ax,ay,az,gx,gy,gz)
    
    ##############################################
    ####### Write a code here to calculate  ######
    ####### PITCH using complementry filter ######
    
    
    angle = atan2( ax , sqrt(ay*ay + az*az)  )
    
    
    alpha = 0.03
    
    
    
    
    
    ##############################################
    
endfunction 

function comp_filter_roll(ax,ay,az,gx,gy,gz)
    
    ##############################################
    ####### Write a code here to calculate #######
    ####### ROLL using complementry filter #######
    
    
    
    
    ##############################################
    
endfunction 






function execute_code()
    global A;
    for n = 1:rows(A)               #do not change this line
        
        ###############################################
        ####### Write a code here to calculate  #######
        ####### PITCH using complementry filter #######
        
        
        read_accel(   A(n,2), A(n,1),A(n,4),A(n,3),A(n,6),A(n,5)    ) ;
        read_gyro (   A(n,8),A(n,7),A(n,10),A(n,9),A(n,12),A(n,11)  );
        
        
        
        
        
        
        
        
        ###############################################
        
    endfor
    
    
    
    
    
    #csvwrite('output_data.csv',B);        #do not change this line
endfunction

execute_code                          #do not change this line
