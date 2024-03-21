// CAN Send Example
//

#include <mcp_can.h>
#include <SPI.h>

MCP_CAN CAN0(10);     // Set CS to pin 10

int photoPin = A0;

void setup()
{
  Serial.begin(115200);

  // Initialize MCP2515 running at 16MHz with a baudrate of 500kb/s and the masks and filters disabled.
  if(CAN0.begin(MCP_ANY, CAN_500KBPS, MCP_16MHZ) == CAN_OK) Serial.println("MCP2515 Initialized Successfully!");
  else Serial.println("Error Initializing MCP2515...");

  CAN0.setMode(MCP_NORMAL);   // Change to normal mode to allow messages to be transmitted
}

byte data_on[8] = {0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07};
byte data_off[8] = {0x07, 0x06, 0x05, 0x04, 0x03, 0x02, 0x01, 0x00};
unsigned char data[8] = {0, 0, 0, 0, 0, 0, 0, 0};

void loop()
{
  int photo = analogRead(photoPin);
  Serial.println("Photo Data: ");
  Serial.println(photo);
  data[7] = photo;
  
  for(int i=0;i<8;i++)
  {
    Serial.print(data[i]);
    Serial.print("  ");
  }
  Serial.println();
  Serial.println("\n---------------------------");

  byte sndStat = CAN0.sendMsgBuf(0x100, 0, 8, data);

  

  //byte sndStat;
  //if(photo < 60){
  //  sndStat = CAN0.sendMsgBuf(0x100, 0, 8, data_off);
  //}
  //else{
  //  sndStat = CAN0.sendMsgBuf(0x100, 0, 8, data_on);
  //}
  
  if(sndStat == CAN_OK){
    Serial.println("Message Sent Successfully!");
  } else {
    Serial.println("Error Sending Message...");
  }
  delay(100);   // send data per 100ms
}

/*********************************************************************************************************
  END FILE
*********************************************************************************************************/
