// CAN Send Long data
//

#include <mcp_can.h>
#include <SPI.h>

MCP_CAN CAN0(10);     // Set CS to pin 10

unsigned char canMsgAlt[8] = {0, 0, 0, 0, 0, 0, 0, 0};
int32_t altData = 1800045;

void setup()
{
  Serial.begin(115200);

  if(CAN0.begin(MCP_ANY, CAN_500KBPS, MCP_16MHZ) == CAN_OK) Serial.println("MCP2515 Initialized Successfully!");
  else Serial.println("Error Initializing MCP2515...");

  CAN0.setMode(MCP_NORMAL);   // Change to normal mode to allow messages to be transmitted
}

void loop()
{
  canMsgAlt[0] = altData;
  canMsgAlt[1] = altData >> 8;
  canMsgAlt[2] = altData >> 16;
  
  CAN0.sendMsgBuf(321, 0, 3, canMsgAlt);

  Serial.println(altData);
  delay(1000);
}
