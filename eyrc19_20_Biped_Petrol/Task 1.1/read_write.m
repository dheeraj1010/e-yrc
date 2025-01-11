clear all
close all
clc
global A = csvread('csv_matter.csv');  #do not change this line

################################################
#######Declare your global variables here#######
global B;
global acc_raw;
global gyro_raw;
global acc_filter;
global gyro_filter;


global pitch_final
global roll_final



################################################
#for the conversion of bits

########################################################


###########################################################

function read_accel(axl,axh,ayl,ayh,azl,azh)  
    global acc_raw
    f_cut = 5 ;
    #################################################
    ####### Write a code here to combine the ########
    #### HIGH and LOW values from ACCELEROMETER #####

    #8bit  to 16bit conversion
    ax = (axh*256+axl);
    ay = (ayh*256+ayl);
    az = (azh*256+azl);
    
    #unsigned to signed bit conversion
    if (ax>32767)
      ax = ax - 65536 ;
    endif
    
    if (ay>32767)
      ay = ay - 65536 ;
    endif
    
    if (az>32767)
      az = az - 65536 ;
    endif
    
   #scaling with scaling coefficient
    ax = ax/16384;
    ay = ay/16384;
    az = az/16384;
    
    
    acc_raw = [ acc_raw ; ax ay az ];

    #################################################
    
    
    ####################################################
    # Call function lowpassfilter(ax,ay,az,f_cut) here #
    
    lowpassfilter(ax,ay,az,f_cut)
    
    ####################################################
    
endfunction

function read_gyro(gxl,gxh,gyl,gyh,gzl,gzh)
    global gyro_raw
    f_cut = 5 ;
    #################################################
    ####### Write a code here to combine the ########
    ###### HIGH and LOW values from GYROSCOPE #######
    
    #8bit  to 16bit conversion
    gx = (gxh*256+gxl);
    gy = (gyh*256+gyl);
    gz = (gzh*256+gzl);
    
     #unsigned to signed bit conversion
    if (gx>32767)
      gx = gx - 65536 ;
    endif
    
    if (gy>32767)
      gy = gy - 65536 ;
    endif
    
    if (gz>32767)
      gz = gz - 65536 ;
    endif
   
    #scaling with scaling coefficient
  
    gx = gx/131;
    gy = gy/131;
    gz = gz/131;
    
    gyro_raw = [ gyro_raw ; gx gy gz ];
    
    #################################################
    
    
    #####################################################
    # Call function highpassfilter(ax,ay,az,f_cut) here #
    
   highpassfilter(gx,gy,gz,f_cut)
    
    #####################################################;
endfunction



function lowpassfilter(ax,ay,az,f_cut)
    dT = 0.01;  #time in seconds
    Tau = 1/(2*pi*f_cut) ;
    alpha = Tau/(Tau+dT);                #do not change this line( changed dT should be in numerator )  
    
    ################################################
    ##############Write your code here##############
    global acc_raw;
    global gyro_raw;
    global acc_filter;
    global gyro_filter;
    global A;
    if rows(acc_filter) ==0 
    acc_filter = [ 0  0 0 ];
    
    else 
    
        ax_fil = (1-alpha)*ax + ( alpha )* acc_filter(rows(acc_filter),1);
        ay_fil = (1-alpha)*ay + ( alpha )* acc_filter(rows(acc_filter),2);
        az_fil = (1-alpha)*az + ( alpha )* acc_filter(rows(acc_filter),3);
        acc_filter = [ acc_filter ; ax_fil ay_fil az_fil ];
 
    endif 
    
    
    
    
    ################################################

endfunction



function highpassfilter(gx,gy,gz,f_cut)
    dT = 0.01;  #time in seconds
    Tau= 1/(2*pi*f_cut) ;
    alpha = Tau/(Tau+dT);                #do not change this line
    
    ################################################
    ##############Write your code here##############
    global acc_raw;
    global gyro_raw;
    global acc_filter;
    global gyro_filter;
    global A;
 
    if rows(gyro_filter) ==0 
    gyro_filter= [  0 0 0 ];
  
    else
   
        gx_fil = (1-alpha)*gyro_filter(rows(gyro_filter),1)+ (1-alpha)*( gx - gyro_raw(rows(gyro_filter),1)  );
        gy_fil= (1-alpha)*gyro_filter(rows(gyro_filter),2)+ (1-alpha)*( gy - gyro_raw(rows(gyro_filter),2)  );
        gz_fil = (1-alpha)*gyro_filter(rows(gyro_filter),3)+ (1-alpha)*( gz - gyro_raw(rows(gyro_filter),3)  );
        
        gyro_filter = [gyro_filter ; gx_fil gy_fil gz_fil   ];
       
    endif 
    
    
    ################################################
    
endfunction

function comp_filter_pitch(ax,ay,az,gx,gy,gz)
   
    global pitch_final;
    dT = 0.01;
    alpha = 0.03; 
    ##############################################
    ####### Write a code here to calculate  ######
    ####### PITCH using complementry filter ######
   
    acc = atan2(ay,abs(az))*(180/pi); 
    
  
      
    # getting final pitch combing both gyro and acc reading  --- 
     if (rows(pitch_final)==0)
      pitch = (1-alpha)*(0 - gx*dT) + alpha*acc;
     else
      pitch = (1-alpha)*(pitch_final(rows(pitch_final)) - gx*dT) + alpha*acc;
     endif
  
    pitch_final = [pitch_final ; pitch];
    
    ##############################################
    
endfunction 

function comp_filter_roll(ax,ay,az,gx,gy,gz)
    
    global roll_final;
    dT = 0.01;
    alpha = 0.03;
    ##############################################
    ####### Write a code here to calculate #######
    ####### ROLL using complementry filter #######
   
    acc = atan2(ax,abs(az))*(180/pi);
    # getting final pitch combing both gyro and acc reading  --- 
    if (rows(roll_final)==0)
     roll = (1-alpha)*(0 - gy*dT) + alpha*acc;
    else
     roll = (1-alpha)*(roll_final(rows(roll_final)) - gy*dT) + alpha*acc;
    endif 
    
     roll_final = [roll_final ; roll];
    
    
    ##############################################
    
endfunction 






function execute_code()
    global A;
    global acc_filter;
    global gyro_filter;
    global pitch_final
    global roll_final

    
    for n = 1:rows(A)               #do not change this line
        
        ###############################################
        ####### Write a code here to calculate  #######
        ####### PITCH using complementry filter #######
        
        
        read_accel(   A(n,2), A(n,1),A(n,4),A(n,3),A(n,6),A(n,5)    ) ;
        read_gyro (   A(n,8),A(n,7),A(n,10),A(n,9),A(n,12),A(n,11)  );
        comp_filter_pitch(acc_filter(n,1),acc_filter(n,2),acc_filter(n,3),gyro_filter(n,1),gyro_filter(n,2),gyro_filter(n,3));
        comp_filter_roll (acc_filter(n,1),acc_filter(n,2),acc_filter(n,3),gyro_filter(n,1),gyro_filter(n,2),gyro_filter(n,3));
        
        
        
        
        
        
        
        ###############################################
        
    endfor
    
    
    global B;
     B  = [pitch_final roll_final];
    csvwrite('output_data.csv',B);        #do not change this line
    

    
endfunction

execute_code                          #do not change this line
