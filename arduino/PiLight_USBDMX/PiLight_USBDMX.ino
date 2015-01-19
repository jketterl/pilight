/*
  Blink
  Turns on an LED on for one second, then off for one second, repeatedly.

  Most Arduinos have an on-board LED you can control. On the Uno and
  Leonardo, it is attached to digital pin 13. If you're unsure what
  pin the on-board LED is connected to on your Arduino model, check
  the documentation at http://arduino.cc

  This example code is in the public domain.

  modified 8 May 2014
  by Scott Fitzgerald
 */

#define F_OSC (16000)

uint16_t 	gCurDmxCh;		//current DMX channel
uint8_t		gDmxState;

enum {BREAK, STARTB, DATA};

// the setup function runs once when you press reset or power the board
void setup() {
  //USART
  UBRR1H  = 0;
  UBRR1L  = ((F_OSC/4000)-1);			//250kbaud, 8N2
  UCSR1C |= (3<<UCSZ10)|(1<<USBS1);
  UCSR1B |= (1<<TXEN1)|(1<<TXCIE1);
  delay(1);
  UDR1    = 0;							//start USART
  
  //Data
  gDmxState= BREAK;					//start with break
  
  pinMode(4, OUTPUT);
  digitalWrite(4, HIGH);
  
  //pinMode(13, OUTPUT);
  
  // set up Timer1: enable overflow interrupt3
  TIMSK1 |= 1 << TOIE1;
  TCCR1A = 0;
}

// send complete interrupt
ISR (USART1_TX_vect) {
  uint8_t DmxState= gDmxState;
  InterfaceConfig c = getInterfaceConfig();

  if (DmxState == BREAK) {
    UBRR1H = 0;
    UBRR1L  = (F_OSC/1600);					//90.9kbaud
    UDR1    = 0;								//send break
    gDmxState= STARTB;
  } else if (DmxState == STARTB) {
    UBRR1H  = 0;
    UBRR1L  = ((F_OSC/4000)-1);				//250kbaud
    UDR1    = 0;								//send start byte
    gDmxState= DATA;
    gCurDmxCh= 0;
  } else {
    if (bit_is_set(c.flags, IBT_ENABLED)) {
      TCNT1 = c.interByteTime;
      TCCR1B = 0x02;
    } else {
      sendNextByte();
    }
  }
}

// timer1 overflow interrupt
ISR (TIMER1_OVF_vect) {
  uint8_t DmxState= gDmxState;
  if (DmxState == BREAK) {
  } else if (DmxState == STARTB) {
  } else {
    sendNextByte();
  }
  TCCR1B = 0;
}

void sendNextByte() {
  uint16_t CurDmxCh= gCurDmxCh;
  UDR1= GetDMXValue(CurDmxCh++);				//send data
  if (CurDmxCh == 512) gDmxState= BREAK; //new break if all ch sent
  else gCurDmxCh= CurDmxCh;
}

// the loop function runs over and over again forever
void loop() {
  delay(1000);
}
