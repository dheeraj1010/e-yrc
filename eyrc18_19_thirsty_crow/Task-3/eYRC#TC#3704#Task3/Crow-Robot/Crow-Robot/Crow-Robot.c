/*
 * Crow-Robot.c
 *
 * Created: 13-12-2018 22:26:14
 * Author : ERTS 1





 * Team Id: 3704
 * Author List:  Akash Yadav,Sachin Kumar
 * Filename: Crow-robot.c
 * Theme: Thirsty Crow
 * Functions: magnet_pin_config(), motor_pin_config(), magnet_on(),magnet_off() ,
              forward() ,backward() ,left() ,soft_left(),right(),soft_right() 
 * Global Variables: None 
 */
  


#define F_CPU 14745600
#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>


 /*
? * Function Name: magnet_pin_config()
? * Input: None
? * Output: None 
? * Logic: This function configures the pins on PORT-H for electromagnet
? * Example Call: magnet_pin_config()
? */
void magnet_pin_config()
{
	DDRH = 0b00000001;
	PORTH =0b00000000;
}




/*
? * Function Name: motor_pin_config()
? * Input: None
? * Output: None
? * Logic: This function configures the pins on PORT-A for Motor driver
? * Example Call: motor_pin_config()
? */
void motor_pin_config()
{
	DDRA = 0b00001111;
	PORTA =0b00000000;
}


/*
? * Function Name: magnet_on()
? * Input: None
? * Output: None
? * Logic: This function turns on electromagnet
? * Example Call: magnet_on()
? */

void magnet_on()
{
	PORTH = 0b00000001;
}

/*
? * Function Name: magnet_off()
? * Input: None
? * Output: None
? * Logic: This function turns off electromagnet
? * Example Call: magnet_off()
? */

void magnet_off()
{
	PORTH = 0b00000000;
}
/*
? * Function Name: forward ()
? * Input: None
? * Output: None
? * Logic: This function moves robot forward
? * Example Call: forward()
? */
void forward()
{
	PORTA =0b00001010 ;
}

/*
? * Function Name: backward()
? * Input: None
? * Output: None
? * Logic: This function moves robot backward
? * Example Call: backward()
? */
void backward()
{
	PORTA =0b00000101 ;
}/*
? * Function Name: left ()
? * Input: None
? * Output: None
? * Logic: This function moves robot left
? * Example Call: left()
? */
void left()
{
	PORTA =0b00000110 ;

}
/*
? * Function Name: right  ()
? * Input: None
? * Output: None
? * Logic: This function moves robot right
? * Example Call: right()
? */
void right()
{
	PORTA =0b00001001 ;
}

/*
? * Function Name: soft_left ()
? * Input: None
? * Output: None
? * Logic: This function moves robot left slowly --( only right motor moves forward )
? * Example Call: soft_left()
? */
void soft_left()
{
	PORTA =0b00000010 ;
}

/*
? * Function Name: soft_right ()
? * Input: None
? * Output: None
? * Logic: This function moves robot right slowly--( only left motor moves forward )
? * Example Call: soft_right()
? */
void soft_right()
{
	PORTA =0b00001000 ;
}
/*
? * Function Name: stop()
? * Input: None
? * Output: None
? * Logic: This function stops both motors 
? * Example Call: stop()
? */
void stop()
{
	PORTA = 0b00000000;
}




int main(void)
{
 
 
 
    /* Replace with your application code */
	motor_pin_config();
	magnet_pin_config();
    while (1) 
    {
		forward();
		_delay_ms(3000);
		stop();
		_delay_ms(2000);
	    magnet_on();
		_delay_ms(3000);
		backward();
		_delay_ms(3000);
		magnet_off();
		stop();
		_delay_ms(3000);
		
    }
}

