// CAN Send Example
//

#include <mcp_can.h>
#include <SPI.h>

MCP_CAN CAN0(10);     // Set CS to pin 10

#define ECHO 7
#define TRIG 4

void setup()
{
  Serial.begin(115200);

  // Initialize MCP2515 running at 16MHz with a baudrate of 500kb/s and the masks and filters disabled.
  if(CAN0.begin(MCP_ANY, CAN_500KBPS, MCP_16MHZ) == CAN_OK) Serial.println("MCP2515 Initialized Successfully!");
  else Serial.println("Error Initializing MCP2515...");

  CAN0.setMode(MCP_NORMAL);   // Change to normal mode to allow messages to be transmitted

  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);
}

unsigned char data[8] = {0, 0, 0, 0, 0, 0, 0, 0};

void loop()
{
  // send data:  ID = 123, Standard CAN Frame, Data length = 8 bytes, 'data' = array of data bytes to send
  byte sndStat = CAN0.sendMsgBuf(0x01, 0, 8, data);
  if(sndStat == CAN_OK){
    Serial.println("Message Sent Successfully!");
    Serial.println();
  } else {
    Serial.println("Error Sending Message...");
  }
  long duration, distance;

  digitalWrite(TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG, LOW);

  duration = pulseIn(ECHO, HIGH);
  distance = duration * 17 /1000;

  data[6] = distance;
  data[7] = distance >> 8;
  
  Serial.print("Distance: ");
  Serial.println(distance);

  int i;
  for(i=0;i<8;i++)
  {
    Serial.print(data[i]);
    Serial.print("  ");
  }
  Serial.println();

  delay(500);   // send data per 100ms
}

/*********************************************************************************************************
  END FILE
*********************************************************************************************************/
