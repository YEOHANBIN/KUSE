// CAN Receive HC-SR04
//

#include <mcp_can.h>
#include <SPI.h>

long unsigned int rxId;
unsigned char len = 0;
unsigned char rxBuf[8];
char msgString[128];                        // Array to store serial string

#define CAN0_INT 2                              // Set INT to pin 2
MCP_CAN CAN0(10);                               // Set CS to pin 10


void setup()
{
  Serial.begin(115200);
  
  if(CAN0.begin(MCP_ANY, CAN_500KBPS, MCP_16MHZ) == CAN_OK)
    Serial.println("MCP2515 Initialized Successfully!");
  else
    Serial.println("Error Initializing MCP2515...");
  
  CAN0.setMode(MCP_NORMAL);

  pinMode(CAN0_INT, INPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  
  Serial.println("MCP2515 Library Receive Example...");
}

void loop()
{
  if(!digitalRead(CAN0_INT))
  {
    CAN0.readMsgBuf(&rxId, &len, rxBuf);
  
    int32_t distance = rxBuf[6];
    distance = (distance<<8)|rxBuf[7];

    if (distance < 255) digitalWrite(LED_BUILTIN, HIGH);
    else digitalWrite(LED_BUILTIN, LOW);
    
    Serial.print("Distance: ");
    Serial.print(distance);
    Serial.print(" mm");  
      
  }
  else{
    Serial.print("Fail");
  }
    Serial.println();
    delay(1000);     
}
  
