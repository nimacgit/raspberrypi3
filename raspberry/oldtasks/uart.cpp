#include <stdio.h>
#include <unistd.h>			
#include <fcntl.h>			
#include <termios.h>		
#include <iostream>
#include <time.h>
#include <socket>
#include <serial>

using namespace std;



int main()
{

	time_t GetTime;
	time(&GetTime);
	//asctime(tmtostr)
	//gmtime(time_t_to_tm)
	struct tm *CurTime = localtime(&GetTime);
	string CurTimestr = ctime(&GetTime);
	cerr << " Hello :) today is " << CurTimestr << " seperate hour: " << CurTime->tm_hour << " and min " << CurTime->tm_min << " and convert all : " << asctime(CurTime) << endl; 

	int uart0_filestream = -1;
	uart0_filestream = open("/dev/ttyS0", O_RDWR | O_NOCTTY | O_NDELAY);

	if (uart0_filestream == -1)
	{
		cout << "Error - Unable to open UART.  Ensure it is not in use by another application" << endl;
		return 0;
	}

//CONFIGURE THE UART
//The flags (defined in /usr/include/termios.h - see http://pubs.opengroup.org/onlinepubs/007908799/xsh/termios.h.html):
//	Baud rate:- B1200, B2400, B4800, B9600, B19200, B38400, B57600, B115200, B230400, B460800, B500000, B576000, B921600, B1000000, B1152000, B1500000, B2000000, B2500000, B3000000, B3500000, B4000000
//	CSIZE:- CS5, CS6, CS7, CS8
//	CLOCAL - Ignore modem status lines
//	CREAD - Enable receiver
//	PARODD - Odd parity (else even)
//	IGNPAR = Ignore characters with parity errors
//	ICRNL - Map CR to NL on input (Use for ASCII comms where you want to auto correct end of line characters - don't use for bianry comms!)
//	PARENB - Parity enable

	struct termios options;
	tcgetattr(uart0_filestream, &options);
	options.c_cflag = B9600 | CS8 | CLOCAL | CREAD;		//<Set baud rate
	options.c_iflag = IGNPAR;
	options.c_oflag = 0;
	options.c_lflag = 0;
	tcflush(uart0_filestream, TCIFLUSH);
	tcsetattr(uart0_filestream, TCSANOW, &options);

//----- Test TX BYTES -----
	unsigned char tx_buffer[20];
	unsigned char *p_tx_buffer;	
	p_tx_buffer = &tx_buffer[0];
	*p_tx_buffer++ = '1';
	*p_tx_buffer++ = '2';
	if (uart0_filestream != -1)
	{
		int count = write(uart0_filestream, &tx_buffer[0], (p_tx_buffer - &tx_buffer[0]));		//Filestream, bytes to write, number of bytes to write
		if (count < 0)
		{
			cout << "UART TX error" << endl;
			return 0;
		}
	}

	//writer:
	string inputstr = "12";
	while(inputstr != "exit")
	{
		write(uart0_filestream, &inputstr[0], inputstr.length());
		cin >> inputstr;
	}
	cerr << "hi" << endl;
//----- CHECK FOR ANY RX BYTES -----
	if (uart0_filestream != -1)
	{
		// Read up to 255 characters from the port if they are there
		unsigned char rx_buffer[256];
		int rx_length = read(uart0_filestream, (void*)rx_buffer, 255);		//Filestream, buffer to store in, number of bytes to read (max)
		if (rx_length < 0)
		{
			//An error occured (will occur if there are no bytes)
			cout << "Error" << endl;
			return 0;
		}
		else
		{
			//Bytes received
			rx_buffer[rx_length] = '\0';
			cout << "bytes read : " << rx_buffer << endl;
		}
	}

//----- CLOSE THE UART -----
	close(uart0_filestream);
}