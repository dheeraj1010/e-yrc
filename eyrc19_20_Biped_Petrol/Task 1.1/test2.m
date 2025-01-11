function [a]=bit_conversion (axh,axl)
    a = axh*256+axl;
    if (a>32767)
      a = a - 65536;
    endif
    return 
endfunction


    ax = bit_conversion(axh,axl);
    ay = bit_conversion(ayh,ayl);
    az = bit_conversion(azh,azl);
    
    16538
    
    gx = bit_conversion(gxh,gxl);
    gy = bit_conversion(gyh,gyl);
    gz = bit_conversion(gzh,gzl);
    
    
     alpha = dT/(Tau+dT)
     
     acc_filter = [ acc_raw(1,1) acc_raw(1,2) acc_raw(1,3) ]
     
     (1/2)*pi*f_cut
     
     gyro_filter= [  gyro_raw(1,1)  gyro_raw(1,2)  gyro_raw(1,3)  ]
     
     
     
     #####pitch_comp_filter
         pitch_acc = atan2( ax , sqrt(ay*ay + az*az)  );
    pitch_gyro = [pitch_gyro ; (pitch_gyro(rows(pitch_gyro))+ (gx*dT)) ] ;
    
    # getting final pitch combing both gyro and acc reading  --- 
    pitch_final = alpha*pitch_acc + (1- alpha)*pitch_gyro;