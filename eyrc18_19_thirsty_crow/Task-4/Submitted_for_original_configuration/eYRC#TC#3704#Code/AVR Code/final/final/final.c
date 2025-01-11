 /*
 
 * final.c 
 * Team Id: 3704
 * Author List:  Akash Yadav,Dheeraj Kumar,Sachin Kumar

 * Filename: final.c
 * Theme: Thirsty Crow
 * Functions: uart0_init() , uart_rx() , uart_tx() ,ISR(),reset_enc() ,motor_speed_control(),
					right_enc(),left_enc(),right(),left(),forward(),backward(),buzzer_on(),buzzer_off(),magnet_on(),magnet_off()
					read_ir(),follow_line()
 * Global Variables: temp,rx_buffer,read_pos,write_pos<comm string ,encoder_1_count, encoder_2_count,string_flag
						adc_result1,adc_result2 ,adc_result3 ,ir1,ir2,ir3
 */
 
#define F_CPU 16000000
#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#define buffer_size 128
#define string_size 3
#define pi 3.1456
#define wheel_rad  3.5
#define width 22

//___________________________________________global variables ______________________________________
unsigned int msg_flag =0;
unsigned char temp;
unsigned char rx_buffer[buffer_size] ;
unsigned int read_pos;
unsigned int write_pos ;
char comm_string[string_size];
unsigned long int comm_string_counter = 0 ;
unsigned int string_flag= 0;
volatile  int encoder1_count  =0;//E4
int wheel_1_rev= 0.0;
volatile long  int encoder2_count  =0;//E7
int wheel_2_rev= 0.0;
float rot1=0.0;
float rot2=0.0;
float dispalcement_1 = 0.0;
float dispalcement_2 = 0.0;
int motor_flag =0;
uint16_t adc_result1, adc_result2,adc_result3;
int ir1,ir2,ir3;

//___________________________________________________________________________________________________

//_________________________________________SERIAL COMM.FUNCTIONS _______________________________________________________

void usart_init () {
	// set baud rate
	// UBRR = ((F_CPU/16*BAUD)-1)
	//for baud rate 9600 -->UBBR = 95
	UBRR0L =0x5F; 							//9600BPS at 14745600Hz
	UBRR0H = 0x00;
	//enable rx and rx
	UCSR0B |= (1<<TXEN0)|(1<<RXEN0) ;//| 1<<TXCIE0| 1<<UDRIE0;
	//set data frame format
	UCSR0C |= (1<<UCSZ00) |(1<< UCSZ01);
	UCSR0B |= (1<<RXCIE0);
}

/*
 * Function Name: uart_tx()
 * Input:char data
 * Output: None 
 * Logic: to send char through serial
 
 */
void uart_tx(unsigned char data) {
	while (!( UCSR0A & (1<<UDRE0)));                // wait while register is free
	UDR0 = data;
}
/*
 * Function Name: send_str()
 * Input: strings 
 * Output: None 
 * Logic: to send string  through serial
 
 */

void send_str(char str[]) {						// for sending strings over serial ...
	int i = 0;
	for (i=0; i<strlen(str); i++) {
		uart_tx(str[i]);
	}
}

unsigned char uart_rx() {
	char chr_rx = '\0';
	if (read_pos!= write_pos) {
		chr_rx = rx_buffer[read_pos];
		read_pos ++;
	}

	if (read_pos>=buffer_size) {
		read_pos =0;
	}

	return chr_rx;
}


ISR(USART0_RX_vect) {
	rx_buffer[write_pos]= UDR0;
	write_pos++;
	if(write_pos>=buffer_size) {
		write_pos =0;
	}

	temp = uart_rx();

//_____________________to be improved .(for receiving strings)______________________________________
	if (string_flag==0) {
		if (temp==':') {
			string_flag =1;
		} else {
			//send_str("AVR CHAR :");
			//uart_tx(temp);
		}
	}

	if ((temp!=':')&&(string_flag==1)) {

		if (temp=='\0') {
			string_flag =0;
			comm_string_counter =0;
		} else {

			comm_string[comm_string_counter]=temp;
			comm_string_counter++;
			if (comm_string_counter>=string_size) {

				//  send_str("AVR STRING :");
				// send_str(comm_string);
				comm_string_counter =0;
				string_flag = 0;
			}
		}
	}
}

//**********************************ENCODERS****************************************

void interrupt_init() {
	DDRE   = 0x00 ;
	PORTE  =0xFF;

	EIMSK |= (1<<INT4)|(1<<INT6);

	EICRB |= (1<<ISC41)|(1<<ISC61);

}


ISR(INT4_vect) {
// cheaking for  forward-backward movement of wheel  ...
	if ((bit_is_clear(PIND,PD5))) {
		//send_str(" 1.B ");
		encoder1_count--;
	} else {
		//send_str(" 1.F");
		encoder1_count++ ;
	}

}
/*
 * Function Name: reset_enc ()
 * Input:
 * Output:
 * Logic: to reset encoder 
 
 */
void reset_enc() {
	encoder1_count =0;
	encoder2_count =0;
}



ISR(INT6_vect) {
// cheaking forward-backward movement of wheel 2 ...

	if (bit_is_clear(PIND,PD7)) {
		//	send_str(" 2.B");
		encoder2_count++;
	} else {
		//	send_str(" 2.F");
		encoder2_count--;
	}

}


//____________________________________ACTUATOR FUNCTIONS _______________________________
//**************motor speed controlling via PWM ************

/*
 * Function Name: motor_speed_control()
 * Input:char data
 * Output: None 
 * Logic:to control motor speed 
 
 */
void motor_speed_control (float m1 , float m2 ) {
	// argument is expected to be in % percentage value .eg; 45...
	// states are modes of operation  as ; f-forward;
	// here using tccr 5 for motor right ...

	TCCR4A =TCCR5A =0b11000010;
	TCCR4B =TCCR5B =0b00011100;
	TCCR4C =TCCR5C =0b00000000;
	ICR4 = ICR5 = 1200;
	OCR4A = ICR4 - ((m1/100)*ICR4);//active_pin
	OCR5A = ICR5 - ((m2/100)*ICR5);//active_pin


	// using tccr 4 for left motor ...
	/*	TCCR4A = 0b11000010;
		TCCR4B = 0b00011100;
		TCCR4C = 0b00000000;
		ICR4  = 3000.0;
		OCR4A = ICR4 - ((active_pin/100)*ICR4);//active_pin

		*/


}
//****************************************************************************************
void magnet_pin_config() {
	DDRH |= 0b00000001;
	PORTH= 0b00000000;
}


void motor_pin_config() {
	DDRA  =0xFF;
	PORTA =0x00;

	DDRL |= 0b00001000;
	DDRH |= 0b00001000;

}
void buzzer_pin_config() {
	DDRH  |=  0b00000010;
	PORTH =  0b00000000;
}

void buzzer_on() {
	PORTH|= 0b00000010;

}
void buzzer_off() {
	PORTH&= 0b11111101;
}
void magnet_on() {
	PORTH|= 0b00000001;
}

void magnet_off() {
	PORTH&= 0b11111110;
}


// motor motion data ....




void right() {
	PORTA =0b00000110 ;

}

void left() {
	PORTA =0b00001001 ;
}

void soft_right() {
	PORTA =0b00000010 ;
}

void soft_left() {
	PORTA =0b00001000 ;
}

void stop() {
	PORTA = 0b00000000;
}

void forward() {

	PORTA =0b00001010;

}

void right_enc(int alpha,int dist) {
	reset_enc();
	int count_d = (int) (270*dist)/(pi*wheel_rad);
	while( (encoder1_count<count_d) || (encoder2_count<count_d) ) {
		forward();
	}

	reset_enc();
	int count = (int)(3*width*alpha)/(4*wheel_rad);
	while ( (encoder1_count<count) || (encoder2_count>-count) ) {
		right();
	}
	temp ='s';
	reset_enc();

}

void left_enc(int alpha,int dist) {
	reset_enc();
	int count_d = (int) (270*dist)/(pi*wheel_rad);
	while( (encoder1_count<count_d) || (encoder2_count<count_d) ) {
		forward();
	}
	reset_enc();
	int count = (int)(3*width*alpha)/(4*wheel_rad);
	while ( (encoder2_count<count) || (encoder1_count>-count) ) {
		left();
	}
	temp='s';
	reset_enc();
}


void backward() {
	PORTA =0b00000101 ;

}

// smart motor handling using encoders ---
void forward_smart(float speed) {
	// arguments are  ( default speed by super-user and encoder gradient )--
	int improve = 10; // constant hit and trial setup --
	reset_enc();
	forward ();
	_delay_ms(10);
	int error = encoder1_count - encoder2_count ;
	motor_speed_control((speed - improve *error ),(speed + improve *error )  ); //  direction  control
	forward();
	_delay_ms(20);

}


/*
 * Function Name:servo_rot()
 * Input:degree
 * Output: None 
 * Logic:to rotate servo at given angle 
 
 */


void servo_rot(int degree) {
	float time = (2.0/225.0)*degree + 0.8;
	DDRB   = 0b00100000;
	TCCR1A = 0b11000010;
	TCCR1B = 0b00011100;
	TCCR1C = 0b00000000;
	ICR1   = 1249;
	OCR1A  = ICR1 - (62.5* time );


}


//*************************************   ADC    **************************************

// initialize adc
void adc_init() {
	// AREF = AVcc
	ADMUX = (1<<REFS0);

	// ADC Enable and prescaler of 128
	// 16000000/128 = 125000
	ADCSRA = (1<<ADEN)|(1<<ADPS2)|(1<<ADPS1)|(1<<ADPS0);
}

// read adc value
uint16_t adc_read(uint8_t ch) {
	// select the corresponding channel 0~7
	// ANDing with '7' will always keep the value
	// of 'ch' between 0 and 7
	ch &= 0b00000111;  // AND operation with 7
	ADMUX = (ADMUX & 0xF8)|ch;     // clears the bottom 3 bits before ORing

	// start single conversion
	// write '1' to ADSC
	ADCSRA |= (1<<ADSC);

	// wait for conversion to complete
	// ADSC becomes '0' again
	// till then, run loop continuously
	while(ADCSRA & (1<<ADSC));

	return (ADC);
}
//*************************************************************************************
void init_devices(void) {
	//disable all interrupts
	cli();
	magnet_pin_config();
	motor_pin_config();
	buzzer_pin_config();
	usart_init();
	adc_init();
	interrupt_init();

	//re-enable interrupts
	sei();
}
int  max (int a,int b, int c) {

	if (a>b && a>c ) {
		return 1 ;
	} else if (b>a && b>c  ) {
		return 2;
	} else if (c>a && c>b  ) {
		return 3 ;
	}

}

/*
 * Function Name: read_ir ()
 * Input:None 
 * Output: None 
 * Logic:to read data from ir sensors
 
 */
void read_ir() {
	if ((adc_result1>740) && (adc_result2 >740) && (adc_result3 >740)) {
		ir1=0;
		ir2=0;
		ir3=0;
	} else if ( adc_result1<580 && adc_result2 <580 && adc_result3 <580) {
		ir1=1;
		ir2=1;
		ir3=1;
	}


	else {
		if ( max( adc_result1,adc_result2,adc_result3) ==1) {
			ir1=0;
			ir2=1;
			ir3=1;
		}
		if ( max ( adc_result1,adc_result2,adc_result3) ==2) {
			ir1=1;
			ir2=0;
			ir3=1;
		}
		if ( max ( adc_result1,adc_result2,adc_result3) ==3) {
			ir1=1;
			ir2=1;
			ir3=0;
		}
	}


	/*


		if (	adc_result1 > 800 ) { ir1 = 0;}
		else if ( adc_result1 <600) { ir1 =1;}

		if (	adc_result2 >800  ) { ir2 = 0;}
		else if ( adc_result2 <600) { ir2 =1;}

		if (	adc_result3 >800  ) { ir3 = 0;}
		else if ( adc_result3 <600) { ir3 =1;}
		*/

}

/*
 * Function Name: follow_line ()
 * Input: None 
 * Output: None 
 * Logic: to follow line 
 
 */

void follow_line() {
	read_ir();
	if ((ir1==1) && (ir2==0) && (ir3==1)) {
		forward();
	}
	if ((ir1==1) && (ir2==1) && (ir3==1)) {
		backward();
	}
	if ((ir1==0) && (ir3==1)) {
		left();
	}
	if ((ir1==1) && (ir3==0)) {
		right();
	}
	if ((ir1==0) && (ir2==0) && (ir3==0)) {
		stop();
		temp='s';
		msg_flag=1;
	}


}



//@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
//                                            VOID  MAIN ()
//@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

int main() {
	cli();
//------------INITIALIZE HARDWARE and PROCESSES  -----------
	init_devices();

//------------ variables declaration  ------------


	char int_buffer[15];
	char ticks[15];
	float speed= 0.0;
	int angle = 20;



	sei();
//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  INFINITE LOOP %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	while (1) {
		//updating wheel revolutions....
		/*if (encoder1_count>=540) {wheel_1_rev++; encoder1_count=0;}
		if (encoder1_count<=-540){wheel_1_rev--; encoder1_count=0;}
		if (encoder2_count>=540) {wheel_2_rev++; encoder2_count=0;}
		if (encoder2_count<=540) {wheel_2_rev--; encoder2_count=0;}
		rot1 = (2*pi*wheel_1_rev + encoder1_count*(2*pi/540) );
		rot2 = (2*pi*wheel_2_rev + encoder2_count*(2*pi/540) );
		dispalcement_1 = (wheel_rad*rot1);
		dispalcement_2 = (wheel_rad*rot2);
		*/
		//setting rotation for servo ...

		angle = atoi(comm_string);
		servo_rot(angle);

		_delay_ms(100);

		if( temp =='+') {
			speed =100.0;
			motor_speed_control(speed,speed-0.5);
		}
		if(temp  =='=') {
			speed= 40.0;
			motor_speed_control(speed,speed+ 11.0);
		}
		if(temp  =='-') {
			speed = 22.0;
			motor_speed_control(speed-0.3,speed);
		}



		adc_result1 = adc_read(1);      // read adc value at PF1
		adc_result2 = adc_read(2);      // read adc value at PF2
		adc_result3 = adc_read(3);      //read ADC value at PF3


		_delay_ms(10);
//#################################################################
		if (msg_flag== 1) {
			uart_tx('!');
		}


//############### ASSIGNING SERIAL VALUES TO MOVEMENTS ############


		switch(temp) {
			case 'f': {

				forward();
				break;
			}
			case 'F': {

				forward();
				_delay_ms(500);
				stop();
				temp = 's';
				break;}
			case 'B': {

				backward();
				_delay_ms(500);
				stop();
				temp='s';
				break;
			}
			case 'b': {
				backward();
				break;
			}
			case 'l': {
				left();
				break;
			}
			case 'r': {
				right();
				break;
			}
			case 'L': {
				left_enc(40,11);
				break;
			}
			case 'R': {
				right_enc(30,11);
				break;
			}
			case 's': {
				stop();
				break;
			}
			case 'S': {
				msg_flag=0;
				break;
			}
			case 'm': {
				magnet_on();
				break;
			}
			case 'n': {
				magnet_off();
				break;
			}
			case'<': {
				soft_left();
				break;
			}
			case '>': {
				soft_right();
				break;
			}
			case'h': {
				buzzer_on();
				_delay_ms(100);
				buzzer_off();
				break;
			}

			case 'w': {

				itoa(adc_result1, int_buffer, 10); // actual ir reading adc conversion ...
				send_str(" left ir:");
				send_str(int_buffer);


				itoa(adc_result2, int_buffer, 10);
				send_str(" middle ir:");
				send_str(int_buffer);


				itoa(adc_result3, int_buffer, 10);
				send_str(" Right ir:");
				send_str(int_buffer);

				break;
			}





			case 'W': {

				read_ir();//reads in 01010101 ir format
				itoa(ir1, int_buffer, 10);
				send_str(" left ir:");
				send_str(int_buffer);


				itoa(ir2, int_buffer, 10);
				send_str(" middle ir:");
				send_str(int_buffer);


				itoa(ir3, int_buffer, 10);
				send_str(" Right ir:");
				send_str(int_buffer);

				break;
			}

			case '#': {
				follow_line();
				break;
			}
			case '1': {
				itoa(encoder1_count,ticks,10);
				send_str(" wheel:1 =");
				send_str(ticks);
				//send_str(encoder1_count);
				break;
			}
			case '2': {
				itoa(encoder2_count,ticks,10);
				send_str(" wheel:2 =");
				send_str(ticks);
				//send_str(encoder2_count);
				break;




			}
		}
	}

}





















